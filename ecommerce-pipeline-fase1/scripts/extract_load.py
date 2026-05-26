"""
Fase 1 — Pipeline E-commerce: Mercado Libre México
Fuente: Selenium + Chrome Headless
Destino: SQLite (local)
"""

import sqlite3
import pandas as pd
from datetime import datetime, UTC
import time
import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

DB_PATH = os.path.join(os.path.dirname(__file__), "../sql/ecommerce.db")

URLS = [
    ("https://listado.mercadolibre.com.mx/celulares-smartphones", "Celulares"),
    ("https://listado.mercadolibre.com.mx/tablets", "Tablets"),
    ("https://listado.mercadolibre.com.mx/laptops-accesorios/laptops", "Laptops"),
    ("https://listado.mercadolibre.com.mx/accesorios-celulares", "Accesorios"),
]


# ─────────────────────────────────────────
# DRIVER  
#          GitHub Actions y máquina local
# ─────────────────────────────────────────
def crear_driver():
    options_chrome = webdriver.ChromeOptions()
    options_edge = Options()
    
    # Si está en GitHub Actions usa Chrome, si no usa Edge
    if os.getenv("GITHUB_ACTIONS"):
        options_chrome.add_argument("--headless")
        options_chrome.add_argument("--no-sandbox")
        options_chrome.add_argument("--disable-dev-shm-usage")
        options_chrome.add_argument("--disable-blink-features=AutomationControlled")
        return webdriver.Chrome(options=options_chrome)
    else:
        options_edge.add_argument("--disable-blink-features=AutomationControlled")
        options_edge.add_argument("--inprivate")
        options_edge.add_experimental_option("excludeSwitches", ["enable-automation"])
        options_edge.add_experimental_option("useAutomationExtension", False)
        return webdriver.Edge(options=options_edge)


# ─────────────────────────────────────────
# 1. EXTRACCIÓN
# ─────────────────────────────────────────
def extraer_pagina(driver, url) -> list:
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    return soup.find_all("li", class_="ui-search-layout__item")


def extract_search_results() -> list:
    driver = crear_driver()
    all_items = []

    for base_url, categoria in URLS:
        offsets = [0, 61, 121, 181]
        for i, offset in enumerate(offsets, 1):
            url = base_url if offset == 0 else f"{base_url}_Desde_{offset}"
            items = extraer_pagina(driver, url)
            for item in items:
                item["categoria"] = categoria
            all_items.extend(items)
            print(f"  📦 {categoria} - Página {i}: {len(items)} productos")
        print(f"  ✅ {categoria} completado")

    driver.quit()
    print(f"  ✅ Total extraído: {len(all_items)} productos")
    return all_items


# ─────────────────────────────────────────
# 2. TRANSFORMACIÓN
# ─────────────────────────────────────────
def limpiar_precio(texto: str) -> float:
    if not texto:
        return None
    try:
        return float(re.sub(r"[^\d]", "", texto))
    except ValueError:
        return None


def transform_data(raw: list) -> pd.DataFrame:
    records = []

    for item in raw:
        titulo_tag      = item.find("a", class_="poly-component__title")
        titulo          = titulo_tag.text.strip() if titulo_tag else None
        url             = titulo_tag["href"] if titulo_tag else None

        img_tag         = item.find("img", class_="poly-component__picture")
        thumbnail       = img_tag["src"] if img_tag else None

        precio_tag = item.select_one(".poly-price__current .andes-money-amount__fraction")
        precio = None
        if precio_tag:
            texto = precio_tag.text.strip()
            if re.sub(r"[,.]", "", texto).isdigit():
                precio = limpiar_precio(texto)

        precio_orig_tag = item.select_one(".andes-money-amount--previous .andes-money-amount__fraction")
        precio_original = None
        if precio_orig_tag:
            texto = precio_orig_tag.text.strip()
            if re.sub(r"[,.]", "", texto).isdigit():
                precio_original = limpiar_precio(texto)

        descuento_tag   = item.select_one(".poly-price__disc_label")
        descuento_pct   = None
        if descuento_tag:
            match = re.search(r"(\d+)%", descuento_tag.text)
            descuento_pct = float(match.group(1)) if match else None

        envio_tag    = item.select_one(".poly-shipping-v2__item .poly-phrase-pill")
        envio_gratis = envio_tag is not None

        rating_tag = item.select_one(".poly-phrase-label")
        rating = None
        if rating_tag:
            try:
                rating = float(rating_tag.text.strip())
            except ValueError:
                rating = None

        records.append({
            "titulo":          titulo,
            "precio":          precio,
            "precio_original": precio_original,
            "descuento_pct":   descuento_pct,
            "moneda":          "MXN",
            "envio_gratis":    envio_gratis,
            "rating":          rating,
            "permalink":       url,
            "thumbnail":       thumbnail,
            "categoria":       item.get("categoria"),
            "extraido_en":     datetime.now(UTC).isoformat()
        })

    df = pd.DataFrame(records)
    df = df.dropna(subset=["precio"])
    print(f"  ✅ Transformación lista: {len(df)} filas, {df.columns.size} columnas")
    return df


# ─────────────────────────────────────────
# 3. CARGA
# ─────────────────────────────────────────
def load_to_sqlite(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)

    try:
        df_existing = pd.read_sql("SELECT titulo FROM productos", conn)
        nuevos = df[~df["titulo"].isin(df_existing["titulo"])]
        print(f"  🔍 Productos nuevos: {len(nuevos)} | Ya existentes: {len(df) - len(nuevos)}")
    except Exception:
        nuevos = df

    if not nuevos.empty:
        nuevos.to_sql(name="productos", con=conn, if_exists="append", index=False)

    conn.close()
    print(f"  ✅ Guardado en {DB_PATH}")


# ─────────────────────────────────────────
# 4. PIPELINE
# ─────────────────────────────────────────
def run_pipeline():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ▶ Iniciando pipeline...")
    raw = extract_search_results()
    df  = transform_data(raw)
    load_to_sqlite(df)
    print(f"  🚀 Pipeline completado\n")


# ─────────────────────────────────────────
# EJECUCIÓN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  E-commerce Pipeline — Mercado Libre MX")
    print(f"  Categorías: Celulares, Tablets, Laptops, Accesorios")
    print("=" * 55)

    try:
        run_pipeline()
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise