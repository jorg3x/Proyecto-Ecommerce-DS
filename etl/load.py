import pandas as pd
from sqlalchemy import create_engine

def cargar_datos(datos_transformados, db_url):
    """
    Se conecta a PostgreSQL y carga los DataFrames transformados en las tablas correspondientes.
    """
    print("\nIniciando la carga de datos a PostgreSQL...")
    
    # Creamos el "motor" de conexión hacia la base de datos
    engine = create_engine(db_url)
    
    try:
        # 1. Cargamos los clientes
        print("Cargando tabla: clientes...")
        # if_exists='append' inserta los datos respetando la estructura de nuestro init.sql
        datos_transformados['clientes'].to_sql('clientes', engine, if_exists='append', index=False)
        
        # 2. Cargamos los productos
        print("Cargando tabla: productos...")
        datos_transformados['productos'].to_sql('productos', engine, if_exists='append', index=False)
        
        # 3. Cargamos las ventas históricas y las predicciones de Prophet
        print("Cargando tabla: predicciones_ventas_diarias...")
        datos_transformados['ventas_diarias'].to_sql('predicciones_ventas_diarias', engine, if_exists='append', index=False)
        
        print("Carga de datos finalizada, Todos los datos están en PostgreSQL.")
        
    except Exception as e:
        print(f"Error durante la carga a la base de datos: {e}")
        print("Si da error de 'llave duplicada', significa que el script ya se corrió antes. Se Deben borrar los datos o recrear el contenedor")