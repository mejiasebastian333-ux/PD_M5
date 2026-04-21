from __future__ import annotations

from pathlib import Path

import pandas as pd


VENTAS_CLEAN_PATH = Path("data/processed/ventas_clean.csv")
PROCESSED_PRODUCTOS_PATH = Path("data/processed/productos_clean.csv")


def build_productos(
    input_path: Path = VENTAS_CLEAN_PATH,
    output_path: Path = PROCESSED_PRODUCTOS_PATH,
) -> pd.DataFrame:
    """Build the products catalog from the cleaned sales data."""
    # Load cleaned sales data
    df_ventas = pd.read_csv(input_path)

    # Extract unique product codes
    productos = df_ventas[['product_code']].drop_duplicates().reset_index(drop=True)

    # Create producto_id autoincremental
    productos['producto_id'] = range(1, len(productos) + 1)

    # Set producto_nombre as product_code
    productos['producto_nombre'] = productos['product_code']

    # Infer categoria from product code prefix
    prefijos = {
        'S10': 'Motorcycles',
        'S12': 'Classic Cars',
        'S18': 'Classic Cars',
        'S24': 'Vintage Cars',
        'S32': 'Ships',
        'S50': 'Trains',
        'S700': 'Planes & Trucks'
    }

    def get_categoria(product_code: str) -> str:
        for prefix, category in prefijos.items():
            if product_code.startswith(prefix):
                return category
        return 'Other'

    productos['categoria'] = productos['product_code'].apply(get_categoria)

    # Reorder columns
    productos = productos[['producto_id', 'producto_nombre', 'categoria']]

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save products data
    productos.to_csv(output_path, index=False)

    return productos


def run() -> pd.DataFrame:
    """Execute the products catalog building step."""
    df = build_productos()
    print("=== Productos Clean Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(10).to_string(index=False))
    print(f"\nArchivo procesado guardado en: {PROCESSED_PRODUCTOS_PATH}")
    return df


if __name__ == "__main__":
    run()