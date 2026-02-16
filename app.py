import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.title("📊 Dashboard de Ventas (Pro)")

@st.cache_data
def load_data():
    df = pd.read_csv("ventas.csv")
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["Total"] = df["Cantidad"] * df["Precio"]
    return df

df = load_data()

# ----- Sidebar (filtros) -----
st.sidebar.header("Filtros")

min_date = df["Fecha"].min().date()
max_date = df["Fecha"].max().date()

rango = st.sidebar.date_input(
    "Rango de fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(rango, tuple) and len(rango) == 2:
    fecha_ini, fecha_fin = rango
else:
    fecha_ini, fecha_fin = min_date, max_date

cats = ["Todas"] + sorted(df["Categoria"].unique().tolist())
cat_sel = st.sidebar.selectbox("Categoría", cats)

# Aplicar filtros
df_f = df[(df["Fecha"].dt.date >= fecha_ini) & (df["Fecha"].dt.date <= fecha_fin)]
if cat_sel != "Todas":
    df_f = df_f[df_f["Categoria"] == cat_sel]

# ----- KPIs -----
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total vendido", f"${df_f['Total'].sum():,.0f}".replace(",", "."))
col2.metric("🧾 Ventas (registros)", int(len(df_f)))
col3.metric("📦 Unidades", int(df_f["Cantidad"].sum()))

st.divider()

# ----- Tabla -----
st.subheader("📋 Detalle")
st.dataframe(df_f.sort_values("Fecha", ascending=False), use_container_width=True)

# ----- Gráficos -----
st.subheader("📈 Ventas por producto")
ventas_producto = df_f.groupby("Producto")["Total"].sum().sort_values(ascending=False)
st.bar_chart(ventas_producto)

st.subheader("📆 Evolución diaria")
ventas_dia = df_f.groupby(df_f["Fecha"].dt.date)["Total"].sum()
st.line_chart(ventas_dia)

st.subheader("🥧 Distribución por categoría")
ventas_cat = df_f.groupby("Categoria")["Total"].sum().sort_values(ascending=False)
st.bar_chart(ventas_cat)
