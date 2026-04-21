# Plan de Desarrollo — Prueba de Desempeño Emausoft
> Construcción de una Solución Analítica End-to-End

---

## Resumen del proyecto

| Campo | Detalle |
|---|---|
| Empresa | Emausoft (SaaS para gestión comercial LATAM) |
| Objetivo | Solución analítica end-to-end: ingesta → EDA → limpieza → carga PostgreSQL → análisis → dashboard |
| Fuentes | CSV Kaggle + 2 APIs públicas + catálogo construido desde ventas |
| Entregables | Dashboard Power BI, código documentado, explicación de decisiones, modelo de datos |
| Stack | Python, Pandas, Requests, PostgreSQL, psycopg2, SQLAlchemy, Power BI |

---

## Estructura del proyecto

```
emausoft_analytics/
├── contexto_pd/
│   └── prueba_desempeno_emausoft.pdf
├── data/
│   ├── raw/                        # Datos originales sin modificar
│   ├── processed/                  # Datos limpios y transformados por fuente
│   └── integrated/                 # Dataset final unificado (todas las fuentes)
├── db/
│   ├── connection.py               # Configuración de conexión a PostgreSQL
│   └── init_db.py                  # Crea las tablas en PostgreSQL si no existen
├── docs/
│   ├── eda_reporte.md              # Generado en Fase 2
│   ├── pipeline_docs.md            # Generado en Fase 7
│   ├── modelado_docs.md            # Generado en Fase 6
│   ├── dashboard_docs.md           # Generado en Fase 7
│   ├── graficos_docs.md            # Generado en Fase 7
│   └── storytelling_docs.md        # Generado en Fase 5
├── outputs/
│   ├── exports/                    # Resultados de queries exportados como CSV
│   └── reportes/                   # Reportes ejecutivos en markdown
├── scripts/
│   ├── ingestion/                  # 01, 02, 03 — carga cruda de fuentes
│   ├── transformation/             # 04, 05, 06, 07 — limpieza por fuente
│   ├── integration/                # 08 — unificación del dataset maestro
│   ├── db/                         # 09 — carga a PostgreSQL
│   ├── analysis/                   # 10, 11, 12 — análisis con pandas y SQL
│   ├── visualization/              # 13 — preparación de datos para Power BI
│   └── pipeline.py                 # Orquestador end-to-end
├── sql/
│   ├── schema.sql                  # Definición del star schema (CREATE TABLE)
│   └── queries.sql                 # Queries para las 8 preguntas de negocio
├── assets/
│   └── star_schema.png             # Diagrama visual del modelo de datos
├── .env                            # Variables de entorno reales (no versionar)
├── .env.example                    # Plantilla de variables de entorno
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## Flujo general

```
[Fase 1] Setup — configurar entorno y variables de conexión
    └── pyproject.toml, .env, .env.example, .gitignore, carpetas
           ↓
[Fase 2] Ingesta — guardar fuentes crudas sin modificar
    ├── 01_load_sales.py        → data/raw/sales_raw.csv
    ├── 02_fetch_clientes.py    → data/raw/clientes_raw.json + clientes_raw.csv
    └── 03_fetch_regiones.py    → data/raw/regiones_raw.json + regiones_raw.csv
           ↓
[Fase 3] EDA — explorar los datos crudos antes de limpiar
    └── 04_eda_raw.py           → docs/eda_reporte.md
           ↓
[Fase 4] Limpieza y transformación — procesar cada fuente por separado
    ├── 05_clean_ventas.py      → data/processed/ventas_clean.csv
    ├── 06_build_productos.py   → data/processed/productos_clean.csv
    ├── 07_clean_clientes.py    → data/processed/clientes_clean.csv
    └── 08_clean_regiones.py    → data/processed/regiones_clean.csv
           ↓
[Fase 5] Integración — unir las 4 fuentes limpias
    └── 09_integrate_master.py  → data/integrated/emausoft_master.csv
           ↓
[Fase 6] Modelado y carga a PostgreSQL — definir schema y cargar datos
    ├── db/connection.py        → módulo reutilizable de conexión
    ├── db/init_db.py           → crea tablas en PostgreSQL (star schema)
    ├── 10_load_to_db.py        → carga emausoft_master.csv a PostgreSQL
    └── sql/schema.sql          → docs/modelado_docs.md + assets/star_schema.png
           ↓
[Fase 7] Análisis (ETL) — análisis con pandas + SQL sobre PostgreSQL
    ├── 11_analisis_negocio.py  → docs/storytelling_docs.md + outputs/reportes/resumen_ejecutivo.md
    └── 12_sql_queries.py       → sql/queries.sql + outputs/exports/
           ↓
[Fase 8] Dashboard — conexión Power BI a PostgreSQL
    └── 13_export_powerbi.py    → outputs/exports/ (tablas para Power BI)
                                   docs/dashboard_docs.md + docs/graficos_docs.md
           ↓
[Fase 9] Orquestación y documentación — entrega final
    ├── pipeline.py             → ejecuta fases 2 a 7 en orden → docs/pipeline_docs.md
    └── README.md               → explicación completa de la solución
```

> **Orden crítico:** el EDA (Fase 3) ocurre sobre los datos crudos, antes de limpiar, para que las decisiones de limpieza estén informadas por los hallazgos exploratorios. La carga a PostgreSQL (Fase 6) ocurre después de la integración, sobre el dataset maestro ya consolidado. El análisis (Fase 7) lee directamente desde PostgreSQL via SQLAlchemy.

---

## Fase 1 — Setup del entorno

### Paso 1 — Configurar el entorno y las variables de conexión

**Archivos:** `pyproject.toml`, `.env`, `.env.example`, `.gitignore`

**Qué hacer:**
1. Crear `pyproject.toml` con todas las dependencias
2. Crear `.env` con los valores reales de conexión a PostgreSQL (no versionar)
3. Crear `.env.example` como plantilla documentada para otros desarrolladores
4. Crear `.gitignore` — ignorar `.env`, `__pycache__/`, y opcionalmente `data/`
5. Crear manualmente todas las carpetas vacías del proyecto

**Contenido de `.env.example`:**
```dotenv
# ─── PostgreSQL ───────────────────────────────────────────
DB_HOST=localhost
DB_PORT=5432
DB_NAME=emausoft_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password

# ─── Configuración general ────────────────────────────────
ENV=development
```

**Contenido de `.env` (valores reales, nunca versionar):**
```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=emausoft_db
DB_USER=postgres
DB_PASSWORD=mi_password_real
ENV=development
```

**Dependencias (`pyproject.toml`):**
```toml
[tool.poetry.dependencies]
python        = "^3.10"
pandas        = "^2.0"
requests      = "^2.31"
psycopg2-binary = "^2.9"
sqlalchemy    = "^2.0"
python-dotenv = "^1.0"
matplotlib    = "^3.8"
seaborn       = "^0.13"
```

> `psycopg2-binary` es el driver de conexión a PostgreSQL desde Python. `sqlalchemy` actúa como ORM/conector para leer y escribir tablas. `matplotlib` y `seaborn` se usan en el EDA.

**Entregable:** Entorno reproducible con variables de conexión configuradas.

---

## Fase 2 — Ingesta de datos

**Principio de esta fase:** cada script carga su fuente tal como llega y la guarda en `data/raw/` sin modificar nada. No se seleccionan columnas, no se renombra, no se filtra. El objetivo es tener una copia fiel de cada fuente original.

---

### Paso 2 — Cargar CSV de ventas

**Archivo:** `scripts/ingestion/01_load_sales.py`
**Fuente:** [Kaggle — sample-sales-data](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)
**Dataset de entrada:** `sales_data_sample.csv` (descargado manualmente y copiado al proyecto)

**Propósito:** leer el archivo tal como viene y guardarlo en `data/raw/` sin tocar nada.

**Qué hacer:**
1. Leer el CSV completo con `pd.read_csv()` — probar sin encoding primero; si falla, usar `encoding='latin-1'`
2. Imprimir reporte de observación:
   - `.shape` → cuántas filas y columnas tiene
   - `.dtypes` → tipo de cada columna
   - `.columns.tolist()` → lista completa de columnas tal como vienen
   - `.head(5)` → primeras filas para ver valores reales
   - `.isnull().sum()` → conteo de nulos por columna (solo observar, no actuar aún)
3. No seleccionar columnas, no renombrar, no filtrar
4. Guardar el DataFrame completo y sin cambios en `data/raw/sales_raw.csv`

**Columnas que trae el CSV original (25 en total):**
```
ORDERNUMBER, QUANTITYORDERED, PRICEEACH, ORDERLINENUMBER, SALES,
ORDERDATE, STATUS, QTR_ID, MONTH_ID, YEAR_ID, PRODUCTLINE, MSRP,
PRODUCTCODE, CUSTOMERNAME, PHONE, ADDRESSLINE1, ADDRESSLINE2,
CITY, STATE, POSTALCODE, COUNTRY, TERRITORY, CONTACTLASTNAME,
CONTACTFIRSTNAME, DEALSIZE
```

> La selección de columnas relevantes (`ORDERNUMBER`, `ORDERDATE`, `PRODUCTCODE`, `QUANTITYORDERED`, `PRICEEACH`, `SALES`, `COUNTRY`) ocurre en el **paso 6** (limpieza). Aquí solo se observan.

**Entregable:** `data/raw/sales_raw.csv` — copia exacta del CSV original.

---

### Paso 3 — Consumir API de clientes

**Archivo:** `scripts/ingestion/02_fetch_clientes.py`
**Fuente:** `https://randomuser.me/api/?results=100`

**Propósito:** llamar a la API y guardar la respuesta completa y cruda en `data/raw/`.

**Qué hacer:**
1. Llamar a la API con `requests.get("https://randomuser.me/api/?results=100")`
2. Verificar que `response.status_code == 200` antes de continuar
3. Parsear el JSON con `.json()` — la respuesta tiene la estructura `{"results": [...], "info": {...}}`
4. Aplanar la lista `results` completa con `pd.json_normalize()` — sin filtrar ningún campo
5. Imprimir reporte de observación:
   - `.shape` → cuántos registros y columnas
   - `.columns.tolist()` → lista completa de campos aplanados
   - `.head(3)` → primeras filas para ver valores reales
6. Guardar la respuesta JSON original en `data/raw/clientes_raw.json`
7. Guardar el DataFrame aplanado completo en `data/raw/clientes_raw.csv`

**Campos que devuelve la API (entre otros):**
```
gender, name.title, name.first, name.last,
location.city, location.country, location.postcode,
location.coordinates.latitude, location.coordinates.longitude,
email, phone, cell, nat, dob.age, picture.medium, ...
```

> La selección de columnas útiles, la unificación del nombre completo y la creación de `cliente_id` ocurren en el **paso 8** (limpieza). Aquí solo se guarda lo que llega de la fuente.

**Entregable:** `data/raw/clientes_raw.json` + `data/raw/clientes_raw.csv` — respuesta completa sin modificar.

---

### Paso 4 — Consumir API de regiones

**Archivo:** `scripts/ingestion/03_fetch_regiones.py`
**Fuente:** `https://restcountries.com/v3.1/all`

**Propósito:** llamar a la API y guardar la respuesta completa y cruda en `data/raw/`.

**Qué hacer:**
1. Llamar a la API con `requests.get("https://restcountries.com/v3.1/all")`
2. Verificar que `response.status_code == 200` antes de continuar
3. Parsear el JSON con `.json()` — lista de ~250 objetos país
4. Aplanar con `pd.json_normalize()` — sin filtrar ningún campo
5. Imprimir reporte de observación:
   - `.shape` → cuántos países y columnas
   - `.columns.tolist()` → lista completa de campos disponibles
   - `.head(3)` → primeras filas para ver valores reales
6. Guardar la respuesta JSON original en `data/raw/regiones_raw.json`
7. Guardar el DataFrame aplanado completo en `data/raw/regiones_raw.csv`

**Campos que devuelve la API (entre otros):**
```
name.common, name.official, cca2, cca3, region, subregion,
capital, languages, currencies, population,
latlng, area, timezones, continents, flags.png, ...
```

> La selección de columnas útiles y la normalización de nombres ocurren en el **paso 9** (limpieza de regiones). Aquí solo se guarda lo que llega de la fuente.

**Entregable:** `data/raw/regiones_raw.json` + `data/raw/regiones_raw.csv` — respuesta completa sin modificar.

---

## Fase 3 — EDA (Análisis Exploratorio)

**Principio de esta fase:** explorar los datos crudos **antes de limpiarlos**, para que las decisiones de limpieza estén fundamentadas en observaciones reales. Los hallazgos del EDA guían directamente qué transformaciones hacer en la Fase 4.

---

### Paso 5 — EDA sobre datos crudos

**Archivo:** `scripts/analysis/04_eda_raw.py`
**Inputs:**
- `data/raw/sales_raw.csv`
- `data/raw/clientes_raw.csv`
- `data/raw/regiones_raw.csv`

**Output:** `docs/eda_reporte.md`

**Qué analizar:**

**5.1 — Dataset de ventas (`sales_raw.csv`):**
1. `.shape`, `.dtypes`, `.describe()`
2. Nulos por columna — identificar si hay columnas críticas con nulos
3. Tipo actual de `ORDERDATE` (viene como string) — documentar que requiere conversión
4. Valores únicos en `COUNTRY` — listar para planificar el mapeo de normalización
5. Distribución de `SALES` — media, mediana, outliers con IQR
6. Evolución de ventas por año (agrupando `YEAR_ID`)
7. Top 10 países por volumen de ventas bruto

**5.2 — Dataset de clientes (`clientes_raw.csv`):**
1. `.shape`, `.columns.tolist()`
2. Identificar los campos que se necesitan: `name.first`, `name.last`, `location.city`, `location.country`
3. Verificar si hay nulos en esos campos clave

**5.3 — Dataset de regiones (`regiones_raw.csv`):**
1. `.shape`, `.columns.tolist()`
2. Identificar los campos que se necesitan: `name.common`, `region`, `subregion`
3. Verificar que `name.common` no tiene nulos

**Decisiones que debe documentar el EDA:**
- Qué columnas del CSV de ventas se descartan y por qué
- Qué columnas de clientes y regiones se conservan
- Qué países del CSV de ventas necesitan normalización (`USA`, `UK`, etc.)
- Si hay duplicados en ventas que deben eliminarse
- Si hay outliers en `SALES` que requieren tratamiento especial

**Entregable:** `docs/eda_reporte.md` — reporte de observaciones con hallazgos por fuente, problemas detectados y decisiones de limpieza que se tomarán en la siguiente fase.

---

## Fase 4 — Limpieza y transformación

**Principio de esta fase:** cada script toma una sola fuente desde `data/raw/`, aplica las transformaciones identificadas en el EDA, y guarda el resultado en `data/processed/`. Ningún script de esta fase hace joins. Los joins ocurren exclusivamente en la Fase 5.

---

### Paso 6 — Limpiar dataset de ventas

**Archivo:** `scripts/transformation/05_clean_ventas.py`
**Input:** `data/raw/sales_raw.csv`
**Output:** `data/processed/ventas_clean.csv`

**Qué hacer:**
1. Cargar `sales_raw.csv`
2. Convertir `ORDERDATE` a datetime con `pd.to_datetime()`
3. Eliminar filas duplicadas con `.drop_duplicates()`
4. Tratar nulos según lo observado en el EDA (eliminar fila o imputar según el caso)
5. Seleccionar solo las columnas relevantes del PDF:
   ```
   ORDERNUMBER, ORDERDATE, PRODUCTCODE, QUANTITYORDERED, PRICEEACH, SALES, COUNTRY
   ```
6. Renombrar columnas a snake_case:
   ```python
   columnas = {
       'ORDERNUMBER':     'order_number',
       'ORDERDATE':       'order_date',
       'PRODUCTCODE':     'product_code',
       'QUANTITYORDERED': 'quantity',
       'PRICEEACH':       'price',
       'SALES':           'sales',
       'COUNTRY':         'country'
   }
   ```
7. Verificar tipos de datos finales y guardar

**Decisiones a documentar:**
- Cómo se tratan los nulos (eliminar fila vs imputar)
- Columnas adicionales del CSV descartadas y justificación

> `product_code` se conserva como clave de texto. El `producto_id` numérico se genera en el paso 7 de forma independiente y se relacionan via join en la Fase 5.

**Entregable:** `data/processed/ventas_clean.csv`

---

### Paso 7 — Construir catálogo de productos

**Archivo:** `scripts/transformation/06_build_productos.py`
**Input:** `data/processed/ventas_clean.csv`
**Output:** `data/processed/productos_clean.csv`

**Propósito:** construir el dataset de productos a partir del CSV de ventas, tal como exige la sección 3.4 del PDF.

**Qué hacer:**
1. Cargar `ventas_clean.csv` y extraer valores únicos de `product_code`
2. Crear `producto_id` numérico autoincremental con `enumerate()` o `pd.factorize()`
3. Inferir `categoria` desde el prefijo del código:
   ```python
   prefijos = {
       'S10':  'Motorcycles',
       'S12':  'Classic Cars',
       'S18':  'Classic Cars',
       'S24':  'Vintage Cars',
       'S32':  'Ships',
       'S50':  'Trains',
       'S700': 'Planes & Trucks'
   }
   df['categoria'] = df['product_code'].apply(
       lambda x: next((v for k, v in prefijos.items() if x.startswith(k)), 'Other')
   )
   ```
4. Armar DataFrame: `producto_id`, `producto_nombre` (= `product_code`), `categoria`
5. Guardar en `data/processed/productos_clean.csv`

**Estructura esperada:**
```
producto_id | producto_nombre | categoria
1           | S10_1678        | Motorcycles
2           | S10_1949        | Motorcycles
3           | S12_1099        | Classic Cars
```

> Este script **no modifica ni re-guarda** `ventas_clean.csv`. El join para obtener `producto_id` ocurre en la integración (paso 10). Condición obligatoria del PDF: `ventas.producto_id ↔ productos.producto_id`.

**Entregable:** `data/processed/productos_clean.csv`

---

### Paso 8 — Limpiar y estructurar clientes

**Archivo:** `scripts/transformation/07_clean_clientes.py`
**Input:** `data/raw/clientes_raw.csv`
**Output:** `data/processed/clientes_clean.csv`

**Qué hacer:**
1. Cargar `clientes_raw.csv`
2. Seleccionar los campos del PDF:
   ```python
   df = df[['name.first', 'name.last', 'location.city', 'location.country']]
   ```
3. Crear `cliente_id` numérico autoincremental (1 al 100):
   ```python
   df['cliente_id'] = range(1, len(df) + 1)
   ```
4. Unificar nombre completo:
   ```python
   df['nombre'] = df['name.first'] + ' ' + df['name.last']
   ```
5. Renombrar columnas: `cliente_id`, `nombre`, `ciudad`, `pais`
6. Limpiar strings con `.str.strip()`
7. Verificar que `cliente_id` sea único y sin nulos
8. Guardar resultado

**Estructura esperada:**
```
cliente_id | nombre        | ciudad    | pais
1          | María López   | Madrid    | Spain
2          | John Smith    | New York  | United States
```

**Condición obligatoria del PDF:** columnas exactas `cliente_id`, `nombre`, `ciudad`, `pais`.

**Entregable:** `data/processed/clientes_clean.csv`

---

### Paso 9 — Limpiar y preparar dataset de regiones

**Archivo:** `scripts/transformation/08_clean_regiones.py`
**Input:** `data/raw/regiones_raw.csv`
**Output:** `data/processed/regiones_clean.csv`

**Propósito:** preparar el dataset de regiones como fuente independiente. El cruce con países de ventas ocurre en la integración.

**Qué hacer:**
1. Cargar `regiones_raw.csv`
2. Seleccionar columnas útiles:
   ```python
   df = df[['name.common', 'region', 'subregion']]
   ```
3. Renombrar: `pais`, `region`, `subregion`
4. Eliminar filas con `pais` nulo o vacío
5. Limpiar strings con `.str.strip()`
6. Guardar resultado

**Estructura esperada:**
```
pais            | region   | subregion
United States   | Americas | Northern America
United Kingdom  | Europe   | Northern Europe
France          | Europe   | Western Europe
```

> La normalización de los nombres de países de ventas (`USA` → `United States`) ocurre en el paso 10 (integración), ya que requiere cruzar dos fuentes.

**Entregable:** `data/processed/regiones_clean.csv`

---

## Fase 5 — Integración

**Principio de esta fase:** unir las 4 fuentes limpias en un único dataset maestro. Aquí se resuelven todas las relaciones entre tablas, la normalización de países y la asignación de clientes a ventas.

---

### Paso 10 — Construir el dataset maestro

**Archivo:** `scripts/integration/09_integrate_master.py`
**Inputs:**
- `data/processed/ventas_clean.csv`
- `data/processed/productos_clean.csv`
- `data/processed/clientes_clean.csv`
- `data/processed/regiones_clean.csv`

**Output:** `data/integrated/emausoft_master.csv`

**Qué hacer:**

**10.1 — Join ventas ↔ productos** (por `product_code`):
```python
df = ventas.merge(productos, left_on='product_code', right_on='producto_nombre', how='left')
# Agrega: producto_id, categoria
```

**10.2 — Normalizar países de ventas y join con regiones:**
```python
mapa_paises = {
    'USA': 'United States',
    'UK':  'United Kingdom',
    ...
}
df['country_norm'] = df['country'].replace(mapa_paises)
df = df.merge(regiones, left_on='country_norm', right_on='pais', how='left')
# Agrega: region, subregion
```

**10.3 — Asignar clientes a ventas** (lógica obligatoria del PDF):
```python
import numpy as np
np.random.seed(42)
df['cliente_id'] = np.random.choice(clientes['cliente_id'].values, size=len(df))
df = df.merge(clientes, on='cliente_id', how='left')
# Agrega: nombre, ciudad, pais (del cliente)
```

**10.4 — Verificar integridad:**
- Sin nulos en columnas clave: `order_number`, `producto_id`, `cliente_id`
- Todos los `producto_id` existen en `productos_clean`
- Todos los `cliente_id` existen en `clientes_clean`
- Imprimir conteo de países sin match en regiones

**10.5 — Guardar dataset maestro**

**Columnas del dataset maestro resultante:**
```
order_number, order_date, product_code, producto_id, producto_nombre,
categoria, quantity, price, sales, country, country_norm, region,
subregion, cliente_id, nombre, ciudad
```

**Decisión a documentar:** justificar la lógica de asignación de clientes y el uso de seed fija.

**Entregable:** `data/integrated/emausoft_master.csv`

---

## Fase 6 — Modelado y carga a PostgreSQL

**Principio de esta fase:** definir el star schema, crear las tablas en PostgreSQL y cargar el dataset maestro. Toda la conexión se maneja exclusivamente a través de las variables de entorno del `.env`.

---

### Paso 11 — Configurar el módulo de conexión a PostgreSQL

**Archivo:** `db/connection.py`

**Propósito:** centralizar la lógica de conexión para que todos los scripts que necesiten acceder a PostgreSQL lo hagan a través de este módulo, leyendo las credenciales desde `.env`.

**Qué hacer:**
1. Leer las variables de entorno con `python-dotenv`
2. Construir la URL de conexión SQLAlchemy
3. Exponer una función `get_engine()` y una función `get_connection()` reutilizables

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

load_dotenv()

DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME")
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    return create_engine(DATABASE_URL)

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
```

**Entregable:** `db/connection.py` — módulo de conexión listo para importar desde cualquier script.

---

### Paso 12 — Definir el star schema y crear tablas en PostgreSQL

**Archivos:** `db/init_db.py`, `sql/schema.sql`, `docs/modelado_docs.md`, `assets/star_schema.png`

**Propósito:** definir el modelo relacional, crear las tablas en PostgreSQL y documentarlo. Cubre el entregable 7.4 del PDF.

**Modelo star schema:**
```
fact_ventas
  ├── order_number   (PK)
  ├── producto_id    (FK → dim_productos)
  ├── cliente_id     (FK → dim_clientes)
  ├── pais_id        (FK → dim_geografia)
  ├── fecha_id       (FK → dim_tiempo)
  ├── quantity
  ├── price
  └── sales

dim_productos:  producto_id, producto_nombre, categoria
dim_clientes:   cliente_id, nombre, ciudad, pais
dim_geografia:  pais_id, pais, country_norm, region, subregion
dim_tiempo:     fecha_id, fecha, anio, mes, trimestre, dia_semana
```

**Qué hacer:**
1. Escribir los `CREATE TABLE` completos en `sql/schema.sql`
2. Crear `db/init_db.py` que lea `sql/schema.sql` y lo ejecute contra PostgreSQL usando `db/connection.py`:
   ```python
   from db.connection import get_connection

   def init_db():
       with open('sql/schema.sql', 'r') as f:
           schema_sql = f.read()
       conn = get_connection()
       cur = conn.cursor()
       cur.execute(schema_sql)
       conn.commit()
       cur.close()
       conn.close()
       print("Tablas creadas correctamente en PostgreSQL.")

   if __name__ == "__main__":
       init_db()
   ```
3. Generar el diagrama visual en dbdiagram.io o draw.io → exportar como `assets/star_schema.png`
4. Redactar `docs/modelado_docs.md` con la descripción de cada tabla, sus columnas, relaciones, granularidad y decisiones de modelado

**Entregables:**
- `sql/schema.sql`
- `db/init_db.py`
- `assets/star_schema.png`
- `docs/modelado_docs.md`

---

### Paso 13 — Cargar el dataset maestro a PostgreSQL

**Archivo:** `scripts/db/10_load_to_db.py`
**Input:** `data/integrated/emausoft_master.csv`
**Output:** Tablas pobladas en PostgreSQL

**Propósito:** cargar el dataset integrado a PostgreSQL, distribuyendo los datos en las tablas del star schema.

**Qué hacer:**
1. Importar `get_engine()` desde `db/connection.py`
2. Cargar `emausoft_master.csv`
3. Construir cada tabla dimensional extrayendo columnas únicas:
   ```python
   from db.connection import get_engine
   engine = get_engine()

   # dim_productos
   dim_productos = master[['producto_id','producto_nombre','categoria']].drop_duplicates()
   dim_productos.to_sql('dim_productos', engine, if_exists='replace', index=False)

   # dim_clientes
   dim_clientes = master[['cliente_id','nombre','ciudad']].drop_duplicates()
   dim_clientes.to_sql('dim_clientes', engine, if_exists='replace', index=False)

   # dim_geografia
   dim_geo = master[['country_norm','region','subregion']].drop_duplicates().reset_index(drop=True)
   dim_geo['pais_id'] = dim_geo.index + 1
   dim_geo.to_sql('dim_geografia', engine, if_exists='replace', index=False)

   # dim_tiempo
   master['fecha_id'] = master['order_date'].dt.strftime('%Y%m%d').astype(int)
   dim_tiempo = master[['fecha_id','order_date']].drop_duplicates()
   dim_tiempo['anio']      = dim_tiempo['order_date'].dt.year
   dim_tiempo['mes']       = dim_tiempo['order_date'].dt.month
   dim_tiempo['trimestre'] = dim_tiempo['order_date'].dt.quarter
   dim_tiempo.to_sql('dim_tiempo', engine, if_exists='replace', index=False)

   # fact_ventas
   fact = master[['order_number','producto_id','cliente_id','fecha_id','quantity','price','sales']]
   fact = fact.merge(dim_geo[['country_norm','pais_id']], on='country_norm', how='left')
   fact.to_sql('fact_ventas', engine, if_exists='replace', index=False)
   ```
4. Verificar la carga: contar filas en cada tabla e imprimir resumen
5. Cerrar conexión

**Verificación esperada:**
```
dim_productos  → N filas (productos únicos)
dim_clientes   → 100 filas
dim_geografia  → N filas (países únicos)
dim_tiempo     → N filas (fechas únicas)
fact_ventas    → N filas (= total de filas en emausoft_master)
```

**Entregable:** Tablas del star schema pobladas en PostgreSQL.

---

## Fase 7 — Análisis (ETL desde PostgreSQL)

**Principio de esta fase:** todos los scripts leen directamente desde PostgreSQL usando SQLAlchemy. El análisis de negocio responde las 8 preguntas del PDF. Las queries SQL complementan con el enfoque relacional exigido por el PDF.

---

### Paso 14 — Responder las 8 preguntas del PDF

**Archivo:** `scripts/analysis/11_analisis_negocio.py`
**Input:** PostgreSQL (via `db/connection.py`)
**Outputs:** `docs/storytelling_docs.md`, `outputs/reportes/resumen_ejecutivo.md`

**Qué hacer:**
1. Conectar a PostgreSQL con `get_engine()`
2. Leer las tablas necesarias con `pd.read_sql()`
3. Estructurar cada pregunta como una función documentada

**Preguntas a responder (sección 5 del PDF):**

| # | Nivel | Pregunta |
|---|---|---|
| 1 | Descriptivo | ¿Cómo han evolucionado las ventas en el tiempo? |
| 2 | Descriptivo | ¿Qué países o regiones generan más ingresos? |
| 3 | Descriptivo | ¿Qué productos tienen mejor desempeño? |
| 4 | Diagnóstico | ¿Qué regiones presentan bajo rendimiento? |
| 5 | Diagnóstico | ¿Qué productos tienen menor impacto en ventas? |
| 6 | Analítico | ¿Qué tipo de clientes generan mayor valor? |
| 7 | Analítico | ¿Existe relación entre ubicación y comportamiento de compra? |
| 8 | Decisión | ¿Qué acciones recomendarías al negocio? |

**Estructura de cada función:**
```python
from db.connection import get_engine
import pandas as pd

engine = get_engine()

def pregunta_1_evolucion_ventas():
    """
    Pregunta: ¿Cómo han evolucionado las ventas en el tiempo?
    Método: join fact_ventas x dim_tiempo, agrupar por mes/año
    Hallazgo: completar tras ejecutar
    """
    query = """
        SELECT dt.anio, dt.mes, ROUND(SUM(fv.sales)::numeric, 2) AS total_ventas
        FROM fact_ventas fv
        JOIN dim_tiempo dt ON fv.fecha_id = dt.fecha_id
        GROUP BY dt.anio, dt.mes
        ORDER BY dt.anio, dt.mes;
    """
    return pd.read_sql(query, engine)
```

**Entregables:**
- `docs/storytelling_docs.md` — hallazgos y recomendaciones por cada pregunta
- `outputs/reportes/resumen_ejecutivo.md` — versión ejecutiva corta para presentación

---

### Paso 15 — Queries SQL directas sobre PostgreSQL

**Archivos:** `scripts/analysis/12_sql_queries.py`, `sql/queries.sql`
**Input:** PostgreSQL (via `db/connection.py`)
**Output:** `outputs/exports/` (un CSV por pregunta), `sql/queries.sql`

**Qué hacer:**
1. Conectar a PostgreSQL con `get_engine()`
2. Escribir una query SQL por cada pregunta de negocio en `sql/queries.sql`
3. Ejecutar cada query desde Python con `pd.read_sql()` y exportar el resultado a `outputs/exports/`

**Ejemplo:**
```sql
-- Pregunta 2: países con más ingresos
SELECT dg.pais, ROUND(SUM(fv.sales)::numeric, 2) AS total_ventas
FROM fact_ventas fv
JOIN dim_geografia dg ON fv.pais_id = dg.pais_id
GROUP BY dg.pais
ORDER BY total_ventas DESC
LIMIT 10;
```

> Este script complementa al paso 14. Ambos responden las mismas preguntas — uno con pandas y otro con SQL puro sobre PostgreSQL — demostrando dominio de los dos enfoques (requerimiento 6.5 del PDF).

**Entregables:**
- `sql/queries.sql`
- CSVs por pregunta en `outputs/exports/`

---

## Fase 8 — Dashboard en Power BI

### Paso 16 — Preparar exports y conectar Power BI a PostgreSQL

**Archivo:** `scripts/visualization/13_export_powerbi.py`
**Input:** PostgreSQL (via `db/connection.py`)
**Outputs:** `outputs/exports/` (tablas listas para Power BI), `docs/dashboard_docs.md`, `docs/graficos_docs.md`

**Propósito:** cubrir el entregable 7.1 del PDF — dashboard funcional y enfocado en negocio que responde las 8 preguntas visualmente.

**Qué hacer en el script:**
1. Conectar a PostgreSQL con `get_engine()`
2. Exportar las tablas del star schema como CSV en `outputs/exports/` (respaldo por si se usa importación directa en Power BI)
3. Documentar la configuración de conexión directa para Power BI

**Conexión directa de Power BI a PostgreSQL:**
```
Origen de datos: PostgreSQL
Servidor:  valor de DB_HOST (ej. localhost o IP del servidor)
Base de datos: valor de DB_NAME (emausoft_db)
Modo: Importar (recomendado para análisis estático)
Tablas a importar: fact_ventas, dim_productos, dim_clientes, dim_geografia, dim_tiempo
```

**Secciones del dashboard Power BI:**

**1. KPIs superiores (tarjetas)**
```
Total ventas ($) | Total órdenes | Países activos | Clientes únicos
```

**2. Evolución de ventas en el tiempo**
- Gráfico de líneas: eje X = mes/año (dim_tiempo), eje Y = SUM(sales)
- Responde pregunta 1

**3. Ventas por país y región**
- Gráfico de barras horizontal — top 10 países por SUM(sales)
- Tabla con regiones de bajo rendimiento
- Responde preguntas 2 y 4

**4. Desempeño de productos**
- Gráfico de barras — top 10 y bottom 10 por SUM(sales)
- Responde preguntas 3 y 5

**5. Perfil de clientes**
- Tabla top clientes por valor total
- Mapa o gráfico de distribución por país del cliente
- Responde preguntas 6 y 7

**6. Recomendaciones**
- Cuadro de texto con hallazgos clave y acciones sugeridas
- Responde pregunta 8

**Entregables:**
- Dashboard `.pbix` funcional con las 8 preguntas respondidas visualmente
- `outputs/exports/` con tablas de respaldo en CSV
- `docs/dashboard_docs.md` — explicación de la app, secciones, filtros, conexión a PostgreSQL y cómo reproducirla
- `docs/graficos_docs.md` — inventario de cada gráfico: tipo, fuente de datos, pregunta de negocio que responde y decisión visual tomada

---

## Fase 9 — Orquestación y documentación

### Paso 17 — Crear el pipeline.py orquestador

**Archivos:** `scripts/pipeline.py`, `docs/pipeline_docs.md`

**Propósito:** ejecutar todo el flujo de datos (fases 2 a 7) con un solo comando. El dashboard Power BI se excluye del pipeline porque es una herramienta interactiva externa.

**Qué hacer:**
1. Importar y ejecutar en orden los scripts de las fases 2 a 7
2. Agregar logging con timestamps por fase
3. Manejar errores con `try/except` — si una fase falla, el pipeline se detiene e informa cuál
4. Imprimir resumen al final: registros procesados y archivos generados

**Estructura básica:**
```python
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s — %(message)s')

def run():
    logging.info("=== FASE 2: Ingesta ===")
    from scripts.ingestion import load_sales, fetch_clientes, fetch_regiones
    load_sales.run(); fetch_clientes.run(); fetch_regiones.run()

    logging.info("=== FASE 3: EDA ===")
    from scripts.analysis import eda_raw
    eda_raw.run()

    logging.info("=== FASE 4: Limpieza ===")
    from scripts.transformation import clean_ventas, build_productos, clean_clientes, clean_regiones
    clean_ventas.run(); build_productos.run(); clean_clientes.run(); clean_regiones.run()

    logging.info("=== FASE 5: Integración ===")
    from scripts.integration import integrate_master
    integrate_master.run()

    logging.info("=== FASE 6: Carga a PostgreSQL ===")
    from db import init_db
    from scripts.db import load_to_db
    init_db.init_db()
    load_to_db.run()

    logging.info("=== FASE 7: Análisis ===")
    from scripts.analysis import analisis_negocio, sql_queries
    analisis_negocio.run(); sql_queries.run()

    logging.info("Pipeline completado.")

if __name__ == "__main__":
    run()
```

**Entregables:**
- `scripts/pipeline.py`
- `docs/pipeline_docs.md` — orden de ejecución, dependencias entre fases, inputs/outputs por fase, cómo manejar errores y cómo reproducir el flujo completo

---

### Paso 18 — Documentar la solución completa

**Archivos:** `README.md`, `docs/storytelling_docs.md`

**Propósito:** cubrir el entregable 7.3 del PDF.

**Contenido obligatorio del README:**
1. **Descripción del caso** — contexto del negocio Emausoft
2. **Estructura del proyecto** — árbol de carpetas con descripción breve de cada una
3. **Requisitos previos** — Python, PostgreSQL instalado, base de datos creada
4. **Instalación y ejecución** — pasos exactos para reproducir el proyecto desde cero:
   ```bash
   git clone <repo>
   cd emausoft_analytics
   poetry install
   cp .env.example .env    # rellenar con credenciales reales
   python scripts/pipeline.py
   # Abrir Power BI y conectar a PostgreSQL
   ```
5. **Variables de entorno** — descripción de cada variable en `.env`
6. **Fuentes de datos** — origen, contenido y forma de acceso a cada fuente
7. **Problemas encontrados y cómo se resolvieron:**
   - Encoding del CSV de ventas (`latin-1`)
   - Nombres de países inconsistentes entre el CSV y restcountries (`USA` vs `United States`)
   - El dataset de ventas no tiene clientes → decisión de asignación aleatoria con seed fija
   - Campos anidados en las respuestas JSON → uso de `pd.json_normalize()`
8. **Decisiones técnicas tomadas:**
   - Lógica de asignación de clientes y justificación
   - Categorías de productos inferidas desde prefijos de código
   - Columnas del CSV descartadas y por qué
   - Por qué el EDA se hace sobre datos crudos (antes de limpiar)
9. **Modelo de datos** — descripción del star schema y referencia a `assets/star_schema.png`
10. **Hallazgos principales** — respuesta resumida a las 8 preguntas
11. **Recomendaciones al negocio**

**Entregable:** `README.md` + `docs/storytelling_docs.md` completos.

---

## Mapa completo de entregables `.md`

| Archivo | Generado en | Contenido |
|---|---|---|
| `docs/eda_reporte.md` | Paso 5 (Fase 3) | Observaciones por fuente, problemas detectados, decisiones de limpieza |
| `docs/modelado_docs.md` | Paso 12 (Fase 6) | Descripción del star schema, tablas, relaciones, granularidad |
| `docs/storytelling_docs.md` | Paso 14 (Fase 7) | Hallazgos y recomendaciones por cada una de las 8 preguntas |
| `docs/pipeline_docs.md` | Paso 17 (Fase 9) | Orden de ejecución, dependencias, inputs/outputs, manejo de errores |
| `docs/dashboard_docs.md` | Paso 16 (Fase 8) | Secciones del dashboard, conexión a PostgreSQL, filtros disponibles |
| `docs/graficos_docs.md` | Paso 16 (Fase 8) | Inventario de gráficos, tipo, fuente, pregunta de negocio que responde |
| `outputs/reportes/resumen_ejecutivo.md` | Paso 14 (Fase 7) | Versión ejecutiva corta de hallazgos para presentación o entrega |
| `README.md` | Paso 18 (Fase 9) | Documentación completa de la solución |

---

## Checklist de entregables (sección 7 del PDF)

| # | Entregable del PDF | Archivos del proyecto | Estado |
|---|---|---|---|
| 7.1 | Dashboard funcional y enfocado en negocio | Dashboard `.pbix` + `docs/dashboard_docs.md` | — |
| 7.2 | Scripts de ingesta | `01_load_sales.py`, `02_fetch_clientes.py`, `03_fetch_regiones.py` | — |
| 7.2 | Scripts de transformación | `05_clean_ventas.py`, `06_build_productos.py`, `07_clean_clientes.py`, `08_clean_regiones.py` | — |
| 7.2 | Script de integración | `09_integrate_master.py` | — |
| 7.2 | Scripts de carga a PostgreSQL | `db/connection.py`, `db/init_db.py`, `10_load_to_db.py` | — |
| 7.2 | Scripts de análisis | `11_analisis_negocio.py`, `12_sql_queries.py` | — |
| 7.2 | Pipeline orquestador | `scripts/pipeline.py` | — |
| 7.3 | Problemas encontrados | `README.md` | — |
| 7.3 | Decisiones tomadas | `README.md` | — |
| 7.3 | Estructura de la información | `README.md` + `docs/modelado_docs.md` | — |
| 7.4 | Diagrama del modelo (opcional) | `sql/schema.sql` + `assets/star_schema.png` + `docs/modelado_docs.md` | — |

---

## Notas finales

- **No existe una única solución correcta.** El evaluador valora el criterio técnico y la lógica aplicada (sección 2 del PDF). Documentar cada decisión es tan importante como el código.
- Las credenciales de PostgreSQL viven **únicamente** en `.env` — nunca se hardcodean en el código ni se versionan.
- El EDA se hace sobre datos **crudos** (antes de limpiar) para que las decisiones de transformación estén informadas por observaciones reales.
- La carga a PostgreSQL ocurre sobre el dataset **maestro integrado**, no sobre las fuentes por separado.
- El análisis en Fase 7 lee **desde PostgreSQL**, no desde CSV, demostrando el flujo ETL completo.
- El dataset de ventas no tiene clientes explícitos — la lógica de asignación aleatoria con `np.random.seed(42)` debe estar justificada en el README.
- El dashboard Power BI no forma parte del `pipeline.py` porque es una herramienta interactiva externa. Se conecta directamente a PostgreSQL.
