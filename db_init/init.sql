-- 1. Tabla Maestra de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente VARCHAR(50) PRIMARY KEY,
    id_unico_cliente VARCHAR(50),
    codigo_postal_cliente INT,
    ciudad_cliente VARCHAR(100),
    estado_cliente VARCHAR(5)
);

-- 2. Tabla Maestra de Vendedores
CREATE TABLE IF NOT EXISTS vendedores (
    id_vendedor VARCHAR(50) PRIMARY KEY,
    codigo_postal_vendedor INT,
    ciudad_vendedor VARCHAR(100),
    estado_vendedor VARCHAR(5)
);

-- 3. Tabla Maestra de Productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto VARCHAR(50) PRIMARY KEY,
    categoria_producto VARCHAR(100),
    longitud_nombre_producto INT,
    longitud_descripcion_producto INT,
    cantidad_fotos_producto INT,
    peso_producto_g INT,
    largo_producto_cm INT,
    alto_producto_cm INT,
    ancho_producto_cm INT
);

-- 4. Tabla de Resultados e Indicadores Consolidados (Para el Dashboard y FastAPI)
-- Aquí el pipeline ETL guardará la historia diaria y las proyecciones de Prophet
CREATE TABLE IF NOT EXISTS predicciones_ventas_diarias (
    fecha_venta DATE PRIMARY KEY,
    total_pedidos INT NOT NULL,
    ingresos_brl NUMERIC(12, 2) NOT NULL,
    ingresos_usd NUMERIC(12, 2) NOT NULL,
    tasa_cambio_usd_brl NUMERIC(10, 4) NOT NULL,
    es_prediccion BOOLEAN DEFAULT FALSE,
    ingresos_predichos_usd NUMERIC(12, 2),
    prediccion_limite_superior_usd NUMERIC(12, 2),
    prediccion_limite_inferior_usd NUMERIC(12, 2)
);

-- Índices optimizados para acelerar las consultas de la API y Streamlit
CREATE INDEX IF NOT EXISTS idx_clientes_estado ON clientes(estado_cliente);
CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria_producto);