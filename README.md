# 🛒 E-commerce Data Pipeline — Mercado Libre

Pipeline automatizado que extrae, transforma y carga datos de productos tecnológicos de Mercado Libre México — Celulares, Tablets, Laptops y Accesorios — y los visualiza en un dashboard web en tiempo real.

---

## 🗺️ Arquitectura

![Arquitectura](assets/arquitectura_pipeline.svg)

---

## 📊 Datos que se extraen

| Campo | Descripción |
|-------|-------------|
| `categoria` | Celulares, Tablets, Laptops, Accesorios |
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

### 🐳 Opción A — Con Docker (recomendado)
Requiere tener [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y mínimo 8GB de RAM.

```bash
# 1. Clonar el repositorio
git clone https://github.com/barvl/mercado-libre-data-pipeline.git
cd mercado-libre-data-pipeline

# 2. Crear archivo .env en la raíz del proyecto
# DATABASE_URL=postgresql://usuario:password@host:5432/postgres

# 3. Levantar todos los contenedores
docker-compose up
```

Esto levanta automáticamente:
- 🕷️ **ml_scraper** — extrae productos de Mercado Libre
- 🐘 **ml_sync** — sincroniza SQLite → PostgreSQL
- 📊 **ml_dashboard** — dashboard en `http://localhost:8501`

---
### 🐍 Opción B — Sin Docker (manual)
Requiere Python 3.11+ y Microsoft Edge instalado.

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear archivo .env en ecommerce-pipeline-fase2/scripts/
# DATABASE_URL=postgresql://usuario:password@host:5432/postgres

# 3. Fase 1 — Extrae datos y guarda en SQLite
python ecommerce-pipeline-fase1/scripts/extract_load.py
# La Fase 2 se sincroniza automáticamente cada hora via GitHub Actions

# 4. Fase 3 — Corre el dashboard web
C:\ruta\a\python.exe -m streamlit run fase_III/scripts/dashboard.py

# 5. Verificar datos en SQLite
python ecommerce-pipeline-fase1/scripts/check_db.py
```

---

## 📁 Estructura del proyecto

```
mercadolibre-pipeline/
├── .github/
│   └── workflows/
│       └── pipleline.yml           ← GitHub Actions (sincronización automática)
│
├── ecommerce-pipeline-fase1/
│   ├── scripts/
│   │   ├── extract_load.py         ← Selenium → SQLite
│   │   └── check_db.py             ← Exploración de datos
│   └── sql/
│       └── ecommerce.db            ← Base de datos local
│
├── ecommerce-pipeline-fase2/
│   ├── scripts/
│   │   ├── extract_load_pg.py      ← SQLite → PostgreSQL
│   │   └── test_conexion.py        ← Prueba de conexión
│   └── sql/
│
├── fase_III/
│   └── scripts/
│       └── dashboard.py            ← Dashboard web Streamlit
│
├── assets/                         ← Screenshots del dashboard
├── Dockerfile                      ← Imagen Docker del proyecto
├── docker-compose.yml              ← Orquestación de contenedores
├── requirements.txt
└── README.md
```

---

## 🛣️ Fases

| Fase | Estado | Descripción |
|------|--------|-------------|
| 1 | ✅ Completa | Selenium → SQLite |
| 2 | ✅ Completa | SQLite → PostgreSQL (Supabase) |
| 3 | ✅ Completa | Dashboard web (Streamlit) |
| 4 | ✅ Completa | Automatización con GitHub Actions + Task Scheduler |
| 5 | ✅ Completa | Dockerización completa |

---


## 🌐 Demo en vivo
[Ver dashboard →](https://mercado-libre-data-pipeline-mrnvvk3epawz8btrq6xtfa.streamlit.app/)

---

## 📸 Screenshots

### KPIs
![KPIs](assets/kpis.png)

### Gráficas
![Graficas](assets/grafica_barras.png)
![Graficas](assets/grafica_circular.png)
![Graficas](assets/grafica_lineas_dispersion.png)

### Tabla de productos
![Tabla](assets/tabla_productos.png)


---

## 📈 Métricas del pipeline

- ~960 productos extraídos por ejecución
- Actualización automática cada 60 minutos
- Tiempo promedio ETL: 4.2 minutos
- +1,000 registros históricos almacenados

---

## 🛠️ Tecnologías

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-59666C?style=flat&logo=python&logoColor=white)

---

## 👤 Autor

**Barbara Badillo**
- LinkedIn: [linkedin.com/in/barbara-badillo](https://www.linkedin.com/in/barbara-badillo/)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

