"""
Fase 2 — Pipeline E-commerce: Celulares en Mercado Libre
Fuente: SQLite (Fase 1)
Destino: PostgreSQL (Supabase)
"""

import sqlite3
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import text
from datetime import datetime, UTC
import time
import os

DATABASE_URL = "postgresql://postgres.udbpzomalscregiythfy:#HolaZayn32@aws-1-us-east-1.pooler.supabase.com:5432/postgres"
SQLITE_PATH  = os.path.join(os.path.dirname(__file__), "../../ecommerce-pipeline-fase1/sql/ecommerce.db")

engine = sa.create_engine(DATABASE_URL)


def crear_tabla():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS productos (
                id               SERIAL PRIMARY KEY,
                titulo           TEXT,
                precio           NUMERIC,
                precio_original  NUMERIC,
                descuento_pct    NUMERIC,
                moneda           VARCHAR(10),
                envio_gratis     BOOLEAN,
                rating           NUMERIC,
                permalink        TEXT,
                thumbnail        TEXT,
                categoria        TEXT,
                extraido_en      TIMESTAMPTZ
            )
        """))
        try:
            conn.execute(text("ALTER TABLE productos ADD COLUMN IF NOT EXISTS categoria TEXT"))
        except:
            pass
        conn.commit()
    print("  ✅ Tabla 'productos' lista en PostgreSQL")


def sync_sqlite_to_postgres():
    """Lee SQLite y sube a PostgreSQL solo los registros nuevos."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ▶ Sincronizando SQLite → PostgreSQL...")

    # Leer SQLite
    conn_sqlite = sqlite3.connect(SQLITE_PATH)
    df_sqlite = pd.read_sql("SELECT * FROM productos", conn_sqlite)
    conn_sqlite.close()

    df_sqlite["envio_gratis"] = df_sqlite["envio_gratis"].astype(bool)

    # Leer títulos ya en PostgreSQL
    with engine.connect() as conn:
        df_pg = pd.read_sql("SELECT titulo FROM productos", conn)

    # Filtrar solo nuevos
    nuevos = df_sqlite[~df_sqlite["titulo"].isin(df_pg["titulo"])]
    print(f"  🔍 En SQLite: {len(df_sqlite)} | En PostgreSQL: {len(df_pg)} | Nuevos: {len(nuevos)}")

    if not nuevos.empty:
        nuevos.to_sql("productos", engine, if_exists="append", index=False)
        print(f"  ✅ {len(nuevos)} registros subidos a PostgreSQL")
    else:
        print("  ✅ PostgreSQL ya está actualizado")

    print(f"  🚀 Sincronización completada\n")


if __name__ == "__main__":
    INTERVALO = 3600
    print("=" * 55)
    print("  Fase 2 — SQLite → PostgreSQL (Supabase)")
    print(f"  Intervalo: cada {INTERVALO // 60} minutos")
    print("=" * 55)

    crear_tabla()

    while True:
        try:
            sync_sqlite_to_postgres()
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print(f"  ⏳ Próxima sincronización en {INTERVALO // 60} minutos...")
        time.sleep(INTERVALO)