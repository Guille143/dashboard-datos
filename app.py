import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Ventas", layout="wide")

st.title("📊 Dashboard de Ventas")

# Datos ejemplo
data = {
    "Producto": ["Manzana", "Banana", "Naranja", "Pera"],
    "Ventas": [120, 90, 150, 70],
    "Precio": [100, 80, 120, 110]
}

df = pd.DataFrame(data)

st.subheader("Tabla de productos")
st.dataframe(df)

st.subheader("Ventas por producto")
st.bar_chart(df.set_index("Producto")["Ventas"])

st.subheader("Precio promedio")
st.metric("💲 Precio promedio", round(df["Precio"].mean(), 2))
