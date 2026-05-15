"""
Utilidad para explorar los datos de ecommerce en SQLite.
Corre esto después de extract_load.py para verificar que todo funciona.
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../sql/ecommerce.db")


def conectar():
    return sqlite3.connect(DB_PATH)


def resumen_general():
    conn = conectar()
    df = pd.read_sql("""
        SELECT
            COUNT(*)                        AS total_registros,
            COUNT(DISTINCT titulo)          AS productos_unicos,
            ROUND(MIN(precio), 2)           AS precio_minimo,
            ROUND(MAX(precio), 2)           AS precio_maximo,
            ROUND(AVG(precio), 2)           AS precio_promedio,
            SUM(CASE WHEN envio_gratis = 1 THEN 1 ELSE 0 END) AS con_envio_gratis
        FROM productos
    """, conn)
    conn.close()
    print("\n📊 Resumen general:")
    print(df.to_string(index=False))


def top_precios():
    conn = conectar()
    df = pd.read_sql("""
        SELECT
            titulo,
            ROUND(precio, 2) AS precio,
            ROUND(precio_original, 2) AS precio_original,
            descuento_pct
        FROM productos
        ORDER BY precio DESC
        LIMIT 10
    """, conn)
    conn.close()
    print("\n💎 Top 10 productos más caros:")
    print(df.to_string(index=False))


def productos_con_descuento():
    conn = conectar()
    df = pd.read_sql("""
        SELECT
            titulo,
            precio,
            precio_original,
            descuento_pct
        FROM productos
        WHERE descuento_pct > 10
        ORDER BY descuento_pct DESC
        LIMIT 10
    """, conn)
    conn.close()
    print("\n🔥 Top 10 productos con mayor descuento:")
    print(df.to_string(index=False))


def rating_promedio():
    conn = conectar()
    df = pd.read_sql("""
        SELECT
            ROUND(AVG(rating), 2) AS rating_promedio,
            COUNT(*) AS total_con_rating
        FROM productos
        WHERE rating IS NOT NULL
    """, conn)
    conn.close()
    print("\n⭐ Estadísticas de rating:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    resumen_general()
    top_precios()
    productos_con_descuento()
    rating_promedio()

