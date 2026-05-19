# 🛒 E-commerce Data Pipeline — Mercado Libre

Pipeline automatizado que extrae, transforma y carga datos de celulares de Mercado Libre México y los visualiza en un dashboard web en tiempo real.

---

## 🗺️ Arquitectura

```
Fase 1: Selenium → SQLite
              ↓
Fase 2: SQLite → PostgreSQL (Supabase)
              ↓
Fase 3: Dashboard web (Streamlit)
              ↓
Fase 4: Apache Airflow (automatización)
              ↓
Fase 5: Docker
```

---

## 📊 Datos que se extraen

| Campo | Descripción |
|-------|-------------|
| `titulo` | Nombre del producto |
| `precio` | Precio actual (MXN) |
| `precio_original` | Precio antes del descuento |
| `descuento_pct` | % de descuento |
| `envio_gratis` | Sí / No |
| `rating` | Calificación del producto |
| `permalink` | URL del producto |
| `thumbnail` | Imagen del producto |
| `extraido_en` | Timestamp de extracción |

---

## ⚙️ Instalación y uso

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Fase 1 — Extrae datos y guarda en SQLite (corre cada hora)
python ecommerce-pipeline-fase1/scripts/extract_load.py

# 3. Fase 2 — Sincroniza SQLite → PostgreSQL (corre cada hora)
python ecommerce-pipeline-fase2/scripts/extract_load_pg.py

# 4. Fase 3 — Corre el dashboard web
streamlit run ecommerce-pipeline-fase3/scripts/dashboard.py

# 5. Verificar datos en SQLite
python ecommerce-pipeline-fase1/scripts/check_db.py
```

---

## 📁 Estructura del proyecto

```
mercadolibre-pipeline/
├── ecommerce-pipeline-fase1/
│   ├── scripts/
│   │   ├── extract_load.py     ← Selenium → SQLite
│   │   └── check_db.py         ← Exploración de datos
│   └── sql/
│       └── ecommerce.db        ← Base de datos local
│
├── ecommerce-pipeline-fase2/
│   ├── scripts/
│   │   ├── extract_load_pg.py  ← SQLite → PostgreSQL
│   │   └── test_conexion.py    ← Prueba de conexión
│   └── sql/
│
├── fase_III/
│   └── scripts/
│        └── dashboard.py        ← Dashboard web Streamlit
│   
├──  requirements.txt
|
└── README.md
```

---

## 🛣️ Fases

| Fase | Estado | Descripción |
|------|--------|-------------|
| 1 | ✅ Completa | Selenium → SQLite |
| 2 | ✅ Completa | SQLite → PostgreSQL (Supabase) |
| 3 | ✅ Completa | Dashboard web (Streamlit) |
| 4 | 🔜 | Automatización con Apache Airflow |
| 5 | 🔜 | Dockerización completa |

---

## 🛠️ Tecnologías

| Herramienta | Uso |
|-------------|-----|
| Python | ETL y scraping |
| Selenium + Edge | Extracción de datos |
| SQLite | Base de datos local |
| PostgreSQL (Supabase) | Base de datos en la nube |
| Streamlit | Dashboard web interactivo |
| Apache Airflow | Automatización |
| Docker | Contenedores |

