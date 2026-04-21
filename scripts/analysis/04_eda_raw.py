from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
DOCS_DIR = Path("docs")

def perform_eda_raw() -> None:
    """Realiza análisis exploratorio en los archivos raw, enfocándose en calidad de datos."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # Cargar datos raw
    sales_df = pd.read_csv(RAW_DIR / "sales_raw.csv")
    clientes_df = pd.read_csv(RAW_DIR / "clientes_raw.csv")
    regiones_df = pd.read_csv(RAW_DIR / "regiones_raw.csv")

    print("=== ANÁLISIS DE CALIDAD DE DATOS - ARCHIVOS RAW ===\n")

    # Análisis de Ventas
    print("1. ANÁLISIS DE VENTAS")
    print(f"   Shape: {sales_df.shape}")
    print(f"   Columnas: {len(sales_df.columns)}")
    print(f"   Tipos de datos:\n{sales_df.dtypes}")

    # Nulos en ventas
    nulls_sales = sales_df.isnull().sum()
    print(f"\n   Valores nulos por columna:\n{nulls_sales[nulls_sales > 0]}")

    # Duplicados
    duplicates_sales = sales_df.duplicated().sum()
    print(f"\n   Filas duplicadas: {duplicates_sales}")

    # Fechas
    print(f"\n   Formato de fechas (ORDERDATE): {sales_df['ORDERDATE'].dtype}")
    print(f"   Rango de fechas: {sales_df['ORDERDATE'].min()} a {sales_df['ORDERDATE'].max()}")

    # Valores únicos y posibles problemas
    print(f"\n   Países únicos: {sales_df['COUNTRY'].nunique()}")
    print(f"   Productos únicos: {sales_df['PRODUCTCODE'].nunique()}")

    # Outliers en ventas
    print(f"\n   Estadísticas de SALES:")
    print(f"   Media: {sales_df['SALES'].mean():.2f}")
    print(f"   Mín: {sales_df['SALES'].min():.2f}")
    print(f"   Máx: {sales_df['SALES'].max():.2f}")
    print(f"   Valores negativos: {(sales_df['SALES'] < 0).sum()}")

    # Análisis de Clientes
    print("\n2. ANÁLISIS DE CLIENTES")
    print(f"   Shape: {clientes_df.shape}")
    print(f"   Columnas: {len(clientes_df.columns)}")

    # Nulos en clientes
    nulls_clientes = clientes_df.isnull().sum()
    print(f"\n   Valores nulos por columna:\n{nulls_clientes[nulls_clientes > 0]}")

    # Estructura anidada
    print(f"\n   Columnas con estructura anidada (ejemplos):")
    print(f"   - name.first, name.last (necesitan unificación)")
    print(f"   - location.city, location.country")

    # Países únicos
    print(f"\n   Países únicos: {clientes_df['location.country'].nunique()}")

    # Análisis de Regiones
    print("\n3. ANÁLISIS DE REGIONES")
    print(f"   Shape: {regiones_df.shape}")
    print(f"   Columnas: {len(regiones_df.columns)}")

    # Nulos en regiones
    nulls_regiones = regiones_df.isnull().sum()
    print(f"\n   Valores nulos por columna:\n{nulls_regiones[nulls_regiones > 0]}")

    # Regiones únicas
    print(f"\n   Regiones únicas: {regiones_df['region'].nunique()}")

    # Problemas identificados
    print("\n=== PROBLEMAS DE CALIDAD IDENTIFICADOS ===")
    print("1. VENTAS:")
    print("   - Nulos en columnas (posiblemente ADDRESSLINE2, STATE, etc.)")
    print("   - Filas duplicadas")
    print("   - Fechas en formato string, necesitan conversión a datetime")
    print("   - Nombres de columnas en mayúsculas, inconsistentes")
    print("   - Columnas innecesarias (muchas direcciones, teléfonos)")
    print("   - Posibles valores negativos en SALES")

    print("\n2. CLIENTES:")
    print("   - Estructura anidada en nombres y ubicaciones")
    print("   - Falta de IDs únicos")
    print("   - Nombres separados en first/last, necesitan unificación")
    print("   - Columnas innecesarias (género, emails, teléfonos, etc.)")

    print("\n3. REGIONES:")
    print("   - Falta subregion (API cambió)")
    print("   - Posibles nulos en pais")
    print("   - Nombres de columnas inconsistentes")

    print("\n4. GENERAL:")
    print("   - Falta de catálogo de productos (se construye de ventas)")
    print("   - Inconsistencias en formatos de datos")
    print("   - Necesidad de normalización y limpieza de strings")

    # Guardar reporte
    with open(DOCS_DIR / "eda_reporte.md", "w") as f:
        f.write("# EDA Reporte - Calidad de Datos en Archivos Raw\n\n")
        f.write("## Problemas de Calidad Identificados\n\n")
        f.write("### 1. Ventas (sales_raw.csv)\n")
        f.write(f"- **Shape**: {sales_df.shape}\n")
        f.write(f"- **Nulos**: {nulls_sales.sum()} total\n")
        f.write(f"- **Duplicados**: {duplicates_sales} filas\n")
        f.write("- **Fechas**: Formato string, necesitan conversión\n")
        f.write("- **Columnas**: 25 columnas, muchas innecesarias\n")
        f.write("- **Nombres**: En mayúsculas, inconsistentes\n")
        f.write("- **Outliers**: Posibles valores negativos en SALES\n\n")

        f.write("### 2. Clientes (clientes_raw.csv)\n")
        f.write(f"- **Shape**: {clientes_df.shape}\n")
        f.write(f"- **Nulos**: {nulls_clientes.sum()} total\n")
        f.write("- **Estructura**: Nombres y ubicaciones anidadas\n")
        f.write("- **IDs**: Falta de identificadores únicos\n")
        f.write("- **Columnas**: 34 columnas, muchas innecesarias\n\n")

        f.write("### 3. Regiones (regiones_raw.csv)\n")
        f.write(f"- **Shape**: {regiones_df.shape}\n")
        f.write(f"- **Nulos**: {nulls_regiones.sum()} total\n")
        f.write("- **Estructura**: Falta subregion\n")
        f.write("- **Consistencia**: Nombres de columnas\n\n")

        f.write("### 4. General\n")
        f.write("- **Catálogo de productos**: No existe, se construye de ventas\n")
        f.write("- **Normalización**: Necesaria en formatos y tipos\n")
        f.write("- **Integridad**: Relaciones entre datasets\n\n")

        f.write("## Soluciones Implementadas en ETL\n\n")
        f.write("### Ventas\n")
        f.write("- Conversión de fechas a datetime\n")
        f.write("- Eliminación de duplicados\n")
        f.write("- Selección de columnas relevantes (7 columnas)\n")
        f.write("- Renombrado a snake_case\n\n")

        f.write("### Clientes\n")
        f.write("- Creación de cliente_id autoincremental\n")
        f.write("- Unificación de nombres (first + last)\n")
        f.write("- Selección de campos esenciales\n")
        f.write("- Limpieza de strings\n\n")

        f.write("### Regiones\n")
        f.write("- Adición de subregion vacía\n")
        f.write("- Eliminación de filas con pais nulo\n")
        f.write("- Limpieza de strings\n\n")

        f.write("### Productos\n")
        f.write("- Extracción de productos únicos de ventas\n")
        f.write("- Creación de producto_id\n")
        f.write("- Inferencia de categorías por prefijo\n")

    print("EDA de calidad completado. Reporte en docs/eda_reporte.md")

def run() -> None:
    """Ejecuta el EDA de calidad."""
    perform_eda_raw()

if __name__ == "__main__":
    run()
