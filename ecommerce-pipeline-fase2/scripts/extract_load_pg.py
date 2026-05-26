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
import os

# ─────────────────────────────────────────
# CONFIGURACIÓN — nunca hardcodear credenciales
# En local: crea un archivo .env y usa python-dotenv
# En GitHub Actions: configura los Secrets en el repo
# ─────────────────────────────────────────
def get_database_url() -> str:
    # Intenta cargar .env si existe (útil en local)
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    url = os.getenv("DATABASE_URL")
    if not url:
        raise EnvironmentError(
            "Variable de entorno DATABASE_URL no encontrada.\n"
            "  - Local: crea un archivo .env con DATABASE_URL=postgresql://...\n"
            "  - GitHub Actions: agrega el Secret en Settings → Secrets → Actions"
        )
    return url


SQLITE_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../ecommerce-pipeline-fase1/sql/ecommerce.db"
)


# ─────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────
def crear_tabla(engine):
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
        except Exception:
            pass
        conn.commit()
    print("  ✅ Tabla 'productos' lista en PostgreSQL")


def sync_sqlite_to_postgres(engine):
    """Lee SQLite y sube a PostgreSQL solo los registros nuevos."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ▶ Sincronizando SQLite → PostgreSQL...")

    conn_sqlite = sqlite3.connect(SQLITE_PATH)
    df_sqlite = pd.read_sql("SELECT * FROM productos", conn_sqlite)
    conn_sqlite.close()

    df_sqlite["envio_gratis"] = df_sqlite["envio_gratis"].astype(bool)

    with engine.connect() as conn:
        df_pg = pd.read_sql("SELECT titulo FROM productos", conn)

    nuevos = df_sqlite[~df_sqlite["titulo"].isin(df_pg["titulo"])]
    print(f"  🔍 En SQLite: {len(df_sqlite)} | En PostgreSQL: {len(df_pg)} | Nuevos: {len(nuevos)}")

    if not nuevos.empty:
        nuevos.to_sql("productos", engine, if_exists="append", index=False)
        print(f"  ✅ {len(nuevos)} registros subidos a PostgreSQL")
    else:
        print("  ✅ PostgreSQL ya está actualizado")

    print("  🚀 Sincronización completada\n")


# ─────────────────────────────────────────
# EJECUCIÓN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Fase 2 — SQLite → PostgreSQL (Supabase)")
    print("=" * 55)

    engine = sa.create_engine(get_database_url())
    crear_tabla(engine)

    try:
        sync_sqlite_to_postgres(engine)
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise