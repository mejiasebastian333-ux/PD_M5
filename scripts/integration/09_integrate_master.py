from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


VENTAS_CLEAN_PATH = Path("data/processed/ventas_clean.csv")
PRODUCTOS_CLEAN_PATH = Path("data/processed/productos_clean.csv")
CLIENTES_CLEAN_PATH = Path("data/processed/clientes_clean.csv")
REGIONES_CLEAN_PATH = Path("data/processed/regiones_clean.csv")
INTEGRATED_MASTER_PATH = Path("data/integrated/emausoft_master.csv")


def integrate_master(
    ventas_path: Path = VENTAS_CLEAN_PATH,
    productos_path: Path = PRODUCTOS_CLEAN_PATH,
    clientes_path: Path = CLIENTES_CLEAN_PATH,
    regiones_path: Path = REGIONES_CLEAN_PATH,
    output_path: Path = INTEGRATED_MASTER_PATH,
) -> pd.DataFrame:
    """Integrate all cleaned datasets into the master dataset."""
    # Load all datasets
    ventas = pd.read_csv(ventas_path)
    productos = pd.read_csv(productos_path)
    clientes = pd.read_csv(clientes_path)
    regiones = pd.read_csv(regiones_path)

    # 9.1 — Join ventas ↔ productos (por product_code)
    df = ventas.merge(productos, left_on='product_code', right_on='producto_nombre', how='left')

    # 9.2 — Normalizar nombres de países de ventas y join con regiones
    mapa_paises = {
        'USA': 'United States',
        'UK': 'United Kingdom',
        'France': 'France',
        'Australia': 'Australia',
        'Norway': 'Norway',
        'Ireland': 'Ireland',
        'Canada': 'Canada',
        'Germany': 'Germany',
        'Denmark': 'Denmark',
        'Sweden': 'Sweden',
        'Finland': 'Finland',
        'Austria': 'Austria',
        'Italy': 'Italy',
        'Spain': 'Spain',
        'Switzerland': 'Switzerland',
        'Belgium': 'Belgium',
        'Netherlands': 'Netherlands',
        'Portugal': 'Portugal',
        'Japan': 'Japan',
        'Singapore': 'Singapore',
        'Philippines': 'Philippines',
        'Hong Kong': 'Hong Kong',
        'New Zealand': 'New Zealand',
        'South Africa': 'South Africa',
        'Brazil': 'Brazil',
        'Argentina': 'Argentina',
        'Chile': 'Chile',
        'Colombia': 'Colombia',
        'Mexico': 'Mexico',
    }
    df['country_norm'] = df['country'].replace(mapa_paises)
    df = df.merge(regiones, left_on='country_norm', right_on='pais', how='left')

    # 9.3 — Asignar clientes a ventas
    np.random.seed(42)  # seed fija para reproducibilidad
    df['cliente_id'] = np.random.choice(clientes['cliente_id'].values, size=len(df))
    df = df.merge(clientes, on='cliente_id', how='left')

    # 9.4 — Verificar integridad
    print("=== Integrity Checks ===")
    print(f"Nulls in order_number: {df['order_number'].isnull().sum()}")
    print(f"Nulls in producto_id: {df['producto_id'].isnull().sum()}")
    print(f"Nulls in cliente_id: {df['cliente_id'].isnull().sum()}")

    # Check if all producto_id exist in productos
    missing_productos = df[~df['producto_id'].isin(productos['producto_id'])]
    print(f"Productos missing: {len(missing_productos)}")

    # Check if all cliente_id exist in clientes
    missing_clientes = df[~df['cliente_id'].isin(clientes['cliente_id'])]
    print(f"Clientes missing: {len(missing_clientes)}")

    # Count countries without match in regions
    no_match = df[df['region'].isnull()]['country_norm'].unique()
    print(f"Countries without region match: {list(no_match)}")

    # 9.5 — Select final columns
    final_columns = [
        'order_number', 'order_date', 'product_code', 'producto_id', 'producto_nombre',
        'categoria', 'quantity', 'price', 'sales', 'country', 'country_norm', 'region',
        'subregion', 'cliente_id', 'nombre', 'ciudad'
    ]
    df = df[final_columns]

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save master dataset
    df.to_csv(output_path, index=False)

    return df


def run() -> pd.DataFrame:
    """Execute the master integration step."""
    df = integrate_master()
    print("=== Master Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(5).to_string(index=False))
    print(f"\nArchivo integrado guardado en: {INTEGRATED_MASTER_PATH}")
    return df


if __name__ == "__main__":
    run()