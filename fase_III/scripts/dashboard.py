import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy as sa

st.set_page_config(
    page_title="E-commerce Pipeline — Mercado Libre",
    page_icon="🛒",
    layout="wide"
)

# ─────────────────────────────────────────
# CONEXIÓN
# ─────────────────────────────────────────
DATABASE_URL = st.secrets["DATABASE_URL"]

@st.cache_data(ttl=3600)
def cargar_datos():
    engine = sa.create_engine(DATABASE_URL)
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM productos", conn)
    return df

df = cargar_datos()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("🛒 E-commerce Data Pipeline — Mercado Libre")
st.markdown("Pipeline automatizado de celulares en Mercado Libre México")
st.divider()

# ─────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Precio Promedio", f"${df['precio'].mean():,.0f} MXN")
with col2:
    st.metric("📦 Total Productos", len(df))
with col3:
    pct_envio = df['envio_gratis'].mean() * 100
    st.metric("🚚 Envío Gratis", f"{pct_envio:.0f}%")
with col4:
    st.metric("⭐ Rating Promedio", f"{df['rating'].mean():.2f}")

st.divider()

# ─────────────────────────────────────────
# GRÁFICAS
# ─────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("💎 Top 10 productos más caros")
    top_caros = df.nlargest(10, "precio")[["titulo", "precio"]]
    top_caros["titulo"] = top_caros["titulo"].str[:40] + "..."
    fig = px.bar(top_caros, x="precio", y="titulo", orientation="h",
                color_discrete_sequence=["#F5D547"])
    fig.update_layout(yaxis_title="", xaxis_title="Precio (MXN)", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔥 Top 10 mayor descuento")
    top_descuento = df.dropna(subset=["descuento_pct"]).nlargest(10, "descuento_pct")[["titulo", "descuento_pct"]]
    top_descuento["titulo"] = top_descuento["titulo"].str[:40] + "..."
    fig2 = px.bar(top_descuento, x="descuento_pct", y="titulo", orientation="h",
                color_discrete_sequence=["#374151"])
    fig2.update_layout(yaxis_title="", xaxis_title="Descuento (%)", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Distribución de precios")
    fig3 = px.histogram(df, x="precio", nbins=20, color_discrete_sequence=["#F5D547"])
    fig3.update_layout(xaxis_title="Precio (MXN)", yaxis_title="Cantidad", bargap=0.15)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🚚 Envío gratis vs No")
    envio_counts = df["envio_gratis"].map({True: "Con envío gratis", False: "Sin envío gratis"}).value_counts()
    fig4 = px.pie(values=envio_counts.values, names=envio_counts.index,
                color_discrete_sequence=["#F5D547", "#374151"], hole=0.4)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

col5, col6 = st.columns(2)

with col5:
    st.subheader("📈 Productos por rango de precio")
    df["rango"] = pd.cut(df["precio"],
                        bins=[0, 2000, 5000, 10000, 25000],
                        labels=["$0-2k", "$2k-5k", "$5k-10k", "$10k+"])
    rango_counts = df["rango"].value_counts().sort_index().reset_index()
    rango_counts.columns = ["Rango", "Cantidad"]
    fig5 = px.line(rango_counts, x="Rango", y="Cantidad",
                color_discrete_sequence=["#F5D547"],
                markers=True)
    fig5.update_traces(
        line=dict(width=2.5),
        marker=dict(size=10, line=dict(color="#374151", width=1.5))
    )
    fig5.update_layout(xaxis_title="Rango de precio", yaxis_title="Cantidad")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("⭐ Rating vs Precio")
    fig6 = px.scatter(df.dropna(subset=["rating"]),
                    x="precio", y="rating",
                    hover_data=["titulo"],
                    color_discrete_sequence=["#F5D547"],
                    trendline="ols")  # línea de tendencia
    fig6.update_traces(
        marker=dict(size=10, opacity=0.7, line=dict(color="#374151", width=1.5)),
        selector=dict(mode="markers")
    )
    fig6.update_traces(
        line=dict(color="#374151", width=2),
        selector=dict(mode="lines")
    )
    fig6.update_layout(
        xaxis_title="Precio (MXN)",
        yaxis_title="Rating",
        yaxis=dict(range=[4.0, 5.1])
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.divider()

# ─────────────────────────────────────────
# Insights
# ─────────────────────────────────────────

st.subheader("💡 Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📦 El **86%** de los productos tiene envío gratis")
with col2:
    st.info("💰 La mayoría de celulares está en el rango **$2k-$5k MXN**")
with col3:
    st.info("⭐ Los productos más caros tienden a tener **mejor rating**")

st.divider()

# ─────────────────────────────────────────
# TABLA
# ─────────────────────────────────────────
st.subheader("📋 Tabla de productos")
tabla = df[["titulo", "precio", "precio_original", "descuento_pct", "envio_gratis", "rating"]].sort_values("precio", ascending=False).copy()

# Renombrar columnas
tabla.columns = ["Título", "Precio (MXN)", "Precio Original (MXN)", "Descuento (%)", "Envío Gratis", "Rating"]

# Reemplazar None/NaN
tabla["Precio Original (MXN)"] = tabla["Precio Original (MXN)"].fillna("-")
tabla["Descuento (%)"] = tabla["Descuento (%)"].fillna("-")
tabla["Rating"] = tabla["Rating"].fillna("-")

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True
)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.markdown("**Fuente:** Mercado Libre México | **Actualización:** cada hora | **Tecnologías:** Python · Selenium · SQLite · PostgreSQL · Streamlit")