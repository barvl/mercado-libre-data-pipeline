# 🛒 E-commerce Data Pipeline — Mercado Libre

Pipeline automatizado que extrae, transforma y carga datos de celulares de Mercado Libre México para análisis en Power BI.

---

## 🗺️ Arquitectura

```
Mercado Libre API → Python ETL → SQLite → Power BI
                                    ↓ (Fase 2)
                               PostgreSQL
                                    ↓ (Fase 3)
                            Apache Airflow
                                    ↓ (Fase 4)
                                 Docker
```

---

## 📊 Datos que se extraen

| Campo | Descripción |
|-------|-------------|
| `titulo` | Nombre del producto |
| `precio` | Precio actual (MXN) |
| `precio_original` | Precio antes del descuento |
| `descuento_pct` | % de descuento calculado |
| `condicion` | Nuevo / Usado |
| `marca` | Apple, Samsung, Xiaomi... |
| `ram_gb` | RAM del dispositivo |
| `almacenamiento` | Capacidad interna |
| `envio_gratis` | Sí / No |
| `vendedor_nombre` | Nickname del vendedor |
| `vendidos` | Unidades vendidas |
| `extraido_en` | Timestamp de extracción |

---

## ⚙️ Instalación y uso

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el pipeline (extrae 200 productos cada hora)
python scripts/extract_load.py

# 3. Verificar los datos
python scripts/check_db.py
```

---

## 📈 Vistas para Power BI

| Vista | Uso sugerido |
|-------|--------------|
| `v_ultimo_precio` | KPIs actuales, tablas |
| `v_precio_por_marca` | Gráfica de barras por marca |
| `v_tendencia_precios` | Línea de tendencia histórica |
| `v_mejores_ofertas` | Tabla de ofertas destacadas |

### Conectar Power BI
1. `Obtener datos` → `Base de datos SQLite`
2. Seleccionar `data/ecommerce.db`
3. Importar las vistas anteriores

---

## 🛣️ Fases

| Fase | Estado | Descripción |
|------|--------|-------------|
| 1 | ✅ Activa | API → Python → SQLite → Power BI |
| 2 | 🔜 | Migración a PostgreSQL |
| 3 | 🔜 | Automatización con Apache Airflow |
| 4 | 🔜 | Dockerización completa |
