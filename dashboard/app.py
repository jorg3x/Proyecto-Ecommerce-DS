import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(page_title="E-Commerce Analytics", layout="wide")

# Conexión a la API (Automática en Docker)
API_URL = os.getenv("API_URL", "http://fastapi_app:8000")

@st.cache_data(ttl=60)
def cargar_datos():
    """Consume la API de FastAPI y devuelve un DataFrame blindado"""
    try:
        respuesta = requests.get(f"{API_URL}/api/predicciones")
        if respuesta.status_code == 200:
            df = pd.DataFrame(respuesta.json()["data"])
            df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
            return df
        else:
            return pd.DataFrame() # Retorna tabla vacía si la API da error
    except Exception as e:
        return pd.DataFrame() # Retorna tabla vacía si no hay conexión

df = cargar_datos()

st.title("Panel de Inteligencia de Negocios - Olist E-Commerce")

# Control de errores en la interfaz
if df is None or df.empty:
    st.error("Conectando con la base de datos... Por favor, recarga la página en unos segundos.")
else:
    # Dividimos los datos en Histórico y Predicción para los gráficos
    df_historico = df[df['es_prediccion'] == False]
    df_prediccion = df[df['es_prediccion'] == True]

    # Creamos las 3 pestañas exigidas por la rúbrica
    tab_gerencia, tab_operaciones, tab_tecnica = st.tabs([
        "Visión Gerencial (Finanzas)", 
        "Visión Operativa", 
        "⚙️ Vista Técnica (Machine Learning)"
    ])
    
    # ---------------- PESTAÑA 1: GERENCIA ----------------
    with tab_gerencia:
        st.subheader("Ingresos Históricos y Proyección a 30 Días (CLP)")
        st.markdown("Visualización estratégica de la demanda futura usando el algoritmo Prophet.")
        
        fig_ingresos = px.line(df, x='fecha_venta', y='ingresos_clp', color='es_prediccion', 
                               color_discrete_map={False: '#1f77b4', True: '#ff7f0e'},
                               labels={'ingresos_clp': 'Ingresos (CLP)', 'fecha_venta': 'Fecha', 'es_prediccion': '¿Es Predicción?'})
        st.plotly_chart(fig_ingresos, use_container_width=True)

    # ---------------- PESTAÑA 2: OPERACIONES ----------------
    with tab_operaciones:
        st.subheader("Volumen de Carga Diaria")
        st.markdown("Cantidad de pedidos procesados por día para dimensionamiento de bodega.")
        
        fig_pedidos = px.bar(df_historico, x='fecha_venta', y='total_pedidos', 
                             labels={'total_pedidos': 'N° de Pedidos', 'fecha_venta': 'Fecha'},
                             color_discrete_sequence=['#2ca02c'])
        st.plotly_chart(fig_pedidos, use_container_width=True)

    # ---------------- PESTAÑA 3: TÉCNICA ----------------
    with tab_tecnica:
        st.subheader("Auditoría del Modelo Predictivo")
        st.markdown("Tabla de datos puros con los intervalos de confianza matemáticos del modelo.")
        
        columnas_tecnicas = ['fecha_venta', 'ingresos_predichos_clp', 'prediccion_limite_inferior_clp', 'prediccion_limite_superior_clp']
        st.dataframe(df_prediccion[columnas_tecnicas].style.format({
            'ingresos_predichos_clp': '${:,.0f}',
            'prediccion_limite_inferior_clp': '${:,.0f}',
            'prediccion_limite_superior_clp': '${:,.0f}'
        }))