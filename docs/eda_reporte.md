# EDA Reporte - Calidad de Datos en Archivos Raw

## Problemas de Calidad Identificados

### 1. Ventas (sales_raw.csv)
- **Shape**: (2823, 25)
- **Nulos**: 5157 total
- **Duplicados**: 0 filas
- **Fechas**: Formato string, necesitan conversión
- **Columnas**: 25 columnas, muchas innecesarias
- **Nombres**: En mayúsculas, inconsistentes
- **Outliers**: Posibles valores negativos en SALES

### 2. Clientes (clientes_raw.csv)
- **Shape**: (100, 34)
- **Nulos**: 32 total
- **Estructura**: Nombres y ubicaciones anidadas
- **IDs**: Falta de identificadores únicos
- **Columnas**: 34 columnas, muchas innecesarias

### 3. Regiones (regiones_raw.csv)
- **Shape**: (100, 3)
- **Nulos**: 1 total
- **Estructura**: Falta subregion
- **Consistencia**: Nombres de columnas

### 4. General
- **Catálogo de productos**: No existe, se construye de ventas
- **Normalización**: Necesaria en formatos y tipos
- **Integridad**: Relaciones entre datasets

## Soluciones Implementadas en ETL

### Ventas
- Conversión de fechas a datetime
- Eliminación de duplicados
- Selección de columnas relevantes (7 columnas)
- Renombrado a snake_case

### Clientes
- Creación de cliente_id autoincremental
- Unificación de nombres (first + last)
- Selección de campos esenciales
- Limpieza de strings

### Regiones
- Adición de subregion vacía
- Eliminación de filas con pais nulo
- Limpieza de strings

### Productos
- Extracción de productos únicos de ventas
- Creación de producto_id
- Inferencia de categorías por prefijo
