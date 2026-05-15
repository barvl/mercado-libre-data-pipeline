"""
Fase 1 — Pipeline E-commerce: Celulares en Mercado Libre
Fuente: Selenium + Edge
Destino: SQLite (local)
"""

import sqlite3
import pandas as pd
from datetime import datetime, UTC
import time
import os
import re

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

DB_PATH  = os.path.join(os.path.dirname(__file__), "../sql/ecommerce.db")
BASE_URL = "https://listado.mercadolibre.com.mx/celulares-smartphones"


# ─────────────────────────────────────────
# DRIVER
# ─────────────────────────────────────────
def crear_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--inprivate")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Edge(options=options)


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

    urls = [
        BASE_URL,
        f"{BASE_URL}_Desde_61",
        f"{BASE_URL}_Desde_121",
        f"{BASE_URL}_Desde_181",
    ]

    for i, url in enumerate(urls, 1):
        items = extraer_pagina(driver, url)
        all_items.extend(items)
        print(f"  📦 Página {i}: {len(items)} productos obtenidos")

    driver.quit()
    print(f"  ✅ Total extraído: {len(all_items)} productos")
    return all_items


# ─────────────────────────────────────────
# 2. TRANSFORMACIÓN
# ─────────────────────────────────────────
def limpiar_precio(texto: str) -> float:
    if not texto:
        return None
    return float(re.sub(r"[^\d]", "", texto))


def transform_data(raw: list) -> pd.DataFrame:
    records = []

    for item in raw:
        titulo_tag      = item.find("a", class_="poly-component__title")
        titulo          = titulo_tag.text.strip() if titulo_tag else None
        url             = titulo_tag["href"] if titulo_tag else None

        img_tag         = item.find("img", class_="poly-component__picture")
        thumbnail       = img_tag["src"] if img_tag else None

        precio_tag      = item.select_one(".poly-price__current .andes-money-amount__fraction")
        precio          = limpiar_precio(precio_tag.text) if precio_tag else None

        precio_orig_tag = item.select_one(".andes-money-amount--previous .andes-money-amount__fraction")
        precio_original = limpiar_precio(precio_orig_tag.text) if precio_orig_tag else None

        descuento_tag   = item.select_one(".poly-price__disc_label")
        descuento_pct   = None
        if descuento_tag:
            match = re.search(r"(\d+)%", descuento_tag.text)
            descuento_pct = float(match.group(1)) if match else None

        envio_tag       = item.select_one(".poly-shipping-v2__item .poly-phrase-pill")
        envio_gratis    = envio_tag is not None

        rating_tag      = item.select_one(".poly-phrase-label")
        rating          = float(rating_tag.text.strip()) if rating_tag else None

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

    # Evitar duplicados por título
    try:
        df_existing = pd.read_sql("SELECT titulo FROM productos", conn)
        nuevos = df[~df["titulo"].isin(df_existing["titulo"])]
        print(f"  🔍 Productos nuevos: {len(nuevos)} | Ya existentes: {len(df) - len(nuevos)}")
    except Exception:
        nuevos = df  # tabla vacía, primera vez

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
    INTERVALO = 3600

    print("=" * 55)
    print("  E-commerce Pipeline — Celulares Mercado Libre MX")
    print(f"  Fuente: Selenium + Edge")
    print(f"  Intervalo: cada {INTERVALO // 60} minutos")
    print("=" * 55)

    while True:
        try:
            run_pipeline()
        except Exception as e:
            print(f"  ❌ Error: {e}")

        print(f"  ⏳ Próxima ejecución en {INTERVALO // 60} minutos...")
        time.sleep(INTERVALO)