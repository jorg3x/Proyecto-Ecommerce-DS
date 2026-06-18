# Sistema End-to-End de Inteligencia de Negocios y Predicción de Demanda

Este proyecto implementa una arquitectura **ETL legítima y un sistema de microservicios dockerizado** para el análisis y predicción de ingresos de un entorno de comercio electrónico, utilizando el dataset público de **Olist**. 

El sistema automatiza la ingesta de datos maestros y transaccionales, realiza conversiones de divisas en tiempo real utilizando una API externa, entrena un modelo de Machine Learning para predecir la demanda futura y distribuye la información a través de una API REST propia hacia un dashboard interactivo adaptado para tres audiencias distintas.

---

## Arquitectura del Sistema

El proyecto está diseñado bajo un enfoque de desacoplamiento absoluto mediante 3 contenedores coordinados por **Docker Compose**:

1. **Base de Datos (PostgreSQL 15):** Almacena los datos maestros estables (`clientes`, `productos`, `vendedores`) e inyecta de forma automatizada los resultados consolidados históricos y predictivos a través del script `init.sql`.
2. **Backend (FastAPI):** Microservicio que expone los endpoints de manera RESTful, abstrayendo la base de datos y sirviendo los datos limpios en formato JSON compatible.
3. **Frontend (Streamlit):** Interfaz gráfica interactiva que consume la API y segmenta la visualización para tres audiencias clave:
   * **Visión Gerencial:** Enfocada en KPIs financieros e ingresos futuros proyectados.
   * **Visión Operativa:** Enfocada en el volumen diario de pedidos para la gestión de inventario y bodega.
   * **Vista Técnica:** Tabla de auditoría con los intervalos de confianza e indicadores del modelo predictivo.

---

##Tecnologías y Librerías Utilizadas

* **Pipeline ETL / ML:** Python 3.10, Pandas, Prophet (Facebook AI), SQLAlchemy, Requests.
* **Base de Datos:** PostgreSQL 15, Psycopg2.
* **Backend API:** FastAPI, Uvicorn.
* **Frontend / Gráficos:** Streamlit, Plotly Express.
* **API Externa de Divisas:** ExchangeRate API (Conversión automatizada de BRL a CLP en tiempo real).

---

## Instrucciones de Despliegue (Paso a Paso)

### 1. Prerrequisitos
* Tener instalado **Docker Desktop** y tenerlo en ejecución.
* Clonar este repositorio en tu máquina local.
* Descargar el dataset de Olist y colocar estrictamente los siguientes archivos dentro de la ruta `data/raw/`:
  * `olist_orders_dataset.csv`
  * `olist_order_items_dataset.csv`
  * `olist_customers_dataset.csv`
  * `olist_products_dataset.csv`

### 2. Levantar la Infraestructura (Docker)
Abre una terminal en la raíz del proyecto y ejecuta el siguiente comando para construir y encender los contenedores en segundo plano:
```bash
docker compose up -d --build
