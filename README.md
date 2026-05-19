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


## 🌐 Demo en vivo
[Ver dashboard →](https://mercado-libre-data-pipeline-mrnvvk3epawz8btrq6xtfa.streamlit.app/)

---

## 📸 Screenshots

### KPIs y Top 10
![KPIs](assets/kpis.png)

### Gráficas
![Graficas](assets/grafica_barras.png)
![Graficas](assets/grafica_circular.png)
![Graficas](assets/grafica_lineas_dispersion.png)

### Tabla de productos
![Tabla](assets/tabla_productos.png)


---

## 🛠️ Tecnologías

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

---

## 👤 Autor

**Barbara Badillo**
- LinkedIn: [linkedin.com/in/barbara-badillo](https://www.linkedin.com/in/barbara-badillo/)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

