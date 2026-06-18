from extract import extraer_csvs, extraer_tipo_cambio
from transform import transformar_datos
from load import cargar_datos

def ejecutar_pipeline():
    print("INICIANDO PIPELINE ETL END-TO-END...")
    print("="*40)
    
    # 1. Fase de Extracción (E)
    datos_crudos = extraer_csvs()
    tasa_cambio = extraer_tipo_cambio()
    
    if datos_crudos is None:
        print("Pipeline detenido por error en extracción.")
        return

    # 2. Fase de Transformación (T)
    datos_listos = transformar_datos(datos_crudos, tasa_cambio)
    
    # 3. Fase de Carga (L)
    # Definimos las credenciales que pusimos en el docker-compose.yml
    db_url = "postgresql://admin:adminpassword@localhost:5432/olist_db"
    
    cargar_datos(datos_listos, db_url)
    
    print("="*40)
    print("PIPELINE EJECUTADO AL 100%. LOS DATOS ESTÁN LISTOS PARA LA API Y EL DASHBOARD.")

if __name__ == "__main__":
    ejecutar_pipeline()