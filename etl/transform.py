import pandas as pd
from prophet import Prophet
import warnings

# Evitamos que Prophet llene la consola de advertencias
warnings.filterwarnings('ignore')

def transformar_datos(datos_crudos, tasa_brl_clp):
    """
    Recibe los DataFrames crudos y la tasa de cambio.
    Limpia, cruza, convierte divisas y genera predicciones con Prophet.
    """
    print("Iniciando transformación de datos y limpieza...")

    # 1. Transformar tabla Clientes (Renombrar a español)
    clientes = datos_crudos['clientes'].copy()
    clientes = clientes.rename(columns={
        'customer_id': 'id_cliente',
        'customer_unique_id': 'id_unico_cliente',
        'customer_zip_code_prefix': 'codigo_postal_cliente',
        'customer_city': 'ciudad_cliente',
        'customer_state': 'estado_cliente'
    })

    # 2. Transformar tabla Productos
    productos = datos_crudos['productos'].copy()
    productos = productos.rename(columns={
        'product_id': 'id_producto',
        'product_category_name': 'categoria_producto',
        'product_name_lenght': 'longitud_nombre_producto',
        'product_description_lenght': 'longitud_descripcion_producto',
        'product_photos_qty': 'cantidad_fotos_producto',
        'product_weight_g': 'peso_producto_g',
        'product_length_cm': 'largo_producto_cm',
        'product_height_cm': 'alto_producto_cm',
        'product_width_cm': 'ancho_producto_cm'
    })

    # 3. Procesar las Ventas Transaccionales (Órdenes + Ítems)
    ordenes = datos_crudos['ordenes'].copy()
    items = datos_crudos['items'].copy()

    # Filtramos para quedarnos solo con pedidos completados ('delivered')
    ordenes = ordenes[ordenes['order_status'] == 'delivered']

    # Convertimos el texto a formato fecha (datetime) y extraemos solo el día
    ordenes['order_purchase_timestamp'] = pd.to_datetime(ordenes['order_purchase_timestamp'])
    ordenes['fecha_venta'] = ordenes['order_purchase_timestamp'].dt.date

    # Cruzamos (Inner Join) las órdenes con sus ítems para saber el valor de cada venta
    ventas = pd.merge(ordenes, items, on='order_id', how='inner')

    # Agrupamos por día para obtener el volumen de pedidos y el ingreso total en Reales (BRL)
    ventas_diarias = ventas.groupby('fecha_venta').agg(
        total_pedidos=('order_id', 'nunique'),
        ingresos_brl=('price', 'sum')
    ).reset_index()

    # Convertimos los ingresos a Pesos Chilenos (CLP) usando el dato de la API
    ventas_diarias['ingresos_clp'] = ventas_diarias['ingresos_brl'] * tasa_brl_clp
    ventas_diarias['tasa_cambio_clp_brl'] = tasa_brl_clp
    ventas_diarias['es_prediccion'] = False

    # 4. MACHINE LEARNING: Predicción con Prophet
    print("Entrenando modelo Prophet para predecir demanda de los próximos 30 días...")
    
    # Prophet exige que las columnas se llamen 'ds' (fecha) e 'y' (valor a predecir)
    df_prophet = ventas_diarias[['fecha_venta', 'ingresos_clp']].rename(columns={'fecha_venta': 'ds', 'ingresos_clp': 'y'})
    
    modelo = Prophet(daily_seasonality=False, yearly_seasonality=True)
    modelo.fit(df_prophet)
    
    # Creamos un dataframe vacío con los próximos 30 días
    futuro = modelo.make_future_dataframe(periods=30)
    prediccion = modelo.predict(futuro)
    
    # Filtramos para quedarnos estrictamente con las fechas del futuro
    fecha_maxima_historica = pd.to_datetime(df_prophet['ds'].max())
    prediccion_futura = prediccion[prediccion['ds'] > fecha_maxima_historica].copy()

    # Le damos a la predicción el formato exacto de nuestra tabla SQL
    prediccion_formato = pd.DataFrame({
        'fecha_venta': prediccion_futura['ds'].dt.date,
        'total_pedidos': 0, # En el futuro no sabemos la cantidad exacta de pedidos, solo estimamos ingresos
        'ingresos_brl': prediccion_futura['yhat'] / tasa_brl_clp,
        'ingresos_clp': prediccion_futura['yhat'],
        'tasa_cambio_clp_brl': tasa_brl_clp,
        'es_prediccion': True,
        'ingresos_predichos_clp': prediccion_futura['yhat'],
        'prediccion_limite_superior_clp': prediccion_futura['yhat_upper'],
        'prediccion_limite_inferior_clp': prediccion_futura['yhat_lower']
    })

    # A las ventas históricas les ponemos nulo en las columnas de predicción (porque ya ocurrieron)
    ventas_diarias['ingresos_predichos_clp'] = None
    ventas_diarias['prediccion_limite_superior_clp'] = None
    ventas_diarias['prediccion_limite_inferior_clp'] = None

    # Unimos el pasado (histórico) con el futuro (predicción) en una sola tabla maestra
    df_final_ventas = pd.concat([ventas_diarias, prediccion_formato], ignore_index=True)

    print("✅ ¡Transformación y predicción finalizadas con éxito!")

    # Retornamos un diccionario con las 3 tablas listas para inyectarse en la Base de Datos
    return {
        'clientes': clientes,
        'productos': productos,
        'ventas_diarias': df_final_ventas
    }