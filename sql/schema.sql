-- Star Schema para Emausoft Analytics en PostgreSQL

-- Dimension: Productos
CREATE TABLE IF NOT EXISTS dim_productos (
    producto_id SERIAL PRIMARY KEY,
    producto_nombre VARCHAR(50) UNIQUE,
    categoria VARCHAR(50)
);

-- Dimension: Clientes
CREATE TABLE IF NOT EXISTS dim_clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ciudad VARCHAR(50),
    pais VARCHAR(50)
);

-- Dimension: Regiones
CREATE TABLE IF NOT EXISTS dim_regiones (
    region_id SERIAL PRIMARY KEY,
    pais VARCHAR(50),
    region VARCHAR(50),
    subregion VARCHAR(50)
);

-- Fact: Ventas
CREATE TABLE IF NOT EXISTS fact_ventas (
    venta_id SERIAL PRIMARY KEY,
    order_number INT,
    order_date DATE,
    product_code VARCHAR(50),
    producto_id INT REFERENCES dim_productos(producto_id),
    categoria VARCHAR(50),
    quantity INT,
    price DECIMAL(10,2),
    sales DECIMAL(10,2),
    country VARCHAR(50),
    country_norm VARCHAR(50),
    region VARCHAR(50),
    subregion VARCHAR(50),
    cliente_id INT REFERENCES dim_clientes(cliente_id),
    nombre VARCHAR(100),
    ciudad VARCHAR(50)
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_fact_ventas_order_date ON fact_ventas(order_date);
CREATE INDEX IF NOT EXISTS idx_fact_ventas_country ON fact_ventas(country);
CREATE INDEX IF NOT EXISTS idx_fact_ventas_categoria ON fact_ventas(categoria);