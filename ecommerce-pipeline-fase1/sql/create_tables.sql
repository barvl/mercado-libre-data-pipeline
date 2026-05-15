-- ─────────────────────────────────────────────────────────
-- Tabla principal
-- ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS productos (
    item_id             TEXT,
    titulo              TEXT,
    precio              REAL,
    precio_original     REAL,
    descuento_pct       REAL,
    moneda              TEXT,
    condicion           TEXT,
    disponibles         INTEGER,
    vendidos            INTEGER,
    envio_gratis        INTEGER,   -- 0 o 1
    permalink           TEXT,
    thumbnail           TEXT,
    marca               TEXT,
    modelo              TEXT,
    ram_gb              TEXT,
    almacenamiento      TEXT,
    sistema_operativo   TEXT,
    vendedor_id         INTEGER,
    vendedor_nombre     TEXT,
    extraido_en         TEXT
);


-- ─────────────────────────────────────────────────────────
-- Vista: último snapshot de cada producto
-- (útil para tarjetas KPI en Power BI)
-- ─────────────────────────────────────────────────────────
CREATE VIEW IF NOT EXISTS v_ultimo_precio AS
SELECT *
FROM productos p
WHERE extraido_en = (
    SELECT MAX(extraido_en)
    FROM productos p2
    WHERE p2.item_id = p.item_id
);


-- ─────────────────────────────────────────────────────────
-- Vista: precio promedio por marca (para gráficas de barras)
-- ─────────────────────────────────────────────────────────
CREATE VIEW IF NOT EXISTS v_precio_por_marca AS
SELECT
    marca,
    COUNT(*)                        AS total_productos,
    ROUND(AVG(precio), 0)           AS precio_promedio,
    ROUND(MIN(precio), 0)           AS precio_minimo,
    ROUND(MAX(precio), 0)           AS precio_maximo,
    SUM(CASE WHEN envio_gratis = 1 THEN 1 ELSE 0 END) AS con_envio_gratis
FROM v_ultimo_precio
WHERE marca IS NOT NULL
GROUP BY marca
ORDER BY total_productos DESC;


-- ─────────────────────────────────────────────────────────
-- Vista: evolución histórica de precios por marca
-- (para gráficas de línea con tendencia)
-- ─────────────────────────────────────────────────────────
CREATE VIEW IF NOT EXISTS v_tendencia_precios AS
SELECT
    DATE(extraido_en)               AS fecha,
    marca,
    ROUND(AVG(precio), 0)           AS precio_promedio,
    COUNT(*)                        AS productos
FROM productos
WHERE marca IS NOT NULL
GROUP BY fecha, marca
ORDER BY fecha DESC;


-- ─────────────────────────────────────────────────────────
-- Vista: productos con mayor descuento (para tabla destacados)
-- ─────────────────────────────────────────────────────────
CREATE VIEW IF NOT EXISTS v_mejores_ofertas AS
SELECT
    titulo,
    marca,
    precio,
    precio_original,
    descuento_pct,
    condicion,
    envio_gratis,
    permalink
FROM v_ultimo_precio
WHERE descuento_pct > 5
ORDER BY descuento_pct DESC
LIMIT 50;
