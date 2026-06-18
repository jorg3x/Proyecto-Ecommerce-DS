from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
import pandas as pd
import json
import os

app = FastAPI(
    title="E-Commerce Analytics API",
    description="API para servir predicciones de ventas y datos transaccionales.",
    version="1.0.0"
)

# Conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:adminpassword@localhost:5432/olist_db")
engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    return {"mensaje": "API de E-Commerce operativa. Ve a /docs para ver los endpoints."}

@app.get("/api/predicciones")
def obtener_predicciones():
    """
    Retorna el histórico de ventas y las predicciones de los próximos 30 días.
    """
    try:
        # Leemos directo de la tabla que creó nuestro ETL
        query = "SELECT * FROM predicciones_ventas_diarias ORDER BY fecha_venta ASC"
        df = pd.read_sql(query, engine)
        
        # Convertimos las fechas a texto
        df['fecha_venta'] = df['fecha_venta'].astype(str)
        
        # --- EL TRUCO DEFINITIVO ---
        # Pandas maneja los NaN de forma nativa a la perfección cuando exporta a string de JSON (los vuelve 'null').
        # Luego, json.loads lo convierte de vuelta a un diccionario de Python 100% limpio y compatible.
        json_string = df.to_json(orient="records")
        datos_json = json.loads(json_string)
        
        return {"data": datos_json}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con la base de datos: {str(e)}")