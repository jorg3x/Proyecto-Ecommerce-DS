import pandas as pd
import requests
import os

def extraer_csvs():
    """
    Extrae los datos crudos desde los archivos CSV locales ubicados en data/raw/
    """
    print("Iniciando extracción de archivos CSV...")
    # Definimos la ruta relativa en este caso usamos la carpeta 'data/raw/' (ahi estan los csv)
    ruta_base = 'data/raw/'
    
    # Diccionario para almacenar todos nuestros DataFrames
    datos = {}
    
    try:
        # 1. Datos Transaccionales (Ventas puras)
        datos['ordenes'] = pd.read_csv(os.path.join(ruta_base, 'olist_orders_dataset.csv'))
        datos['items'] = pd.read_csv(os.path.join(ruta_base, 'olist_order_items_dataset.csv'))
        
        # 2. Datos Maestros (Los que luego insertaremos en PostgreSQL)
        datos['clientes'] = pd.read_csv(os.path.join(ruta_base, 'olist_customers_dataset.csv'))
        datos['productos'] = pd.read_csv(os.path.join(ruta_base, 'olist_products_dataset.csv'))
        
        print("CSVs extraídos con éxito a la memoria")
        return datos
        
    except FileNotFoundError as e:
        print(f"Error crítico: No se encontró un archivo CSV. Detalle: {e}")
        print("Deberian estar los archivos de Kaggle en la carpeta 'data/raw/'")
        return None

def extraer_tipo_cambio():
    """
    Se conecta a una API pública para obtener el tipo de cambio actual BRL -> CLP
    """
    print("Conectando a la API de ExchangeRate para obtener BRL a CLP...")
    # Esta API es pública, no requiere key y soporta Peso Chileno (CLP)
    url = "https://open.er-api.com/v6/latest/BRL"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status() 
        
        data = respuesta.json()
        tasa_brl_clp = data['rates']['CLP']
        
        print(f"Tipo de cambio obtenido 1 BRL = {tasa_brl_clp} CLP")
        return tasa_brl_clp
        
    except requests.exceptions.RequestException as e:
        print(f"Advertencia: Falló la conexión con la API: {e}")
        # Valor de respaldo (Fallback): 1 Real = 170 Pesos Chilenos aprox
        return 170.00