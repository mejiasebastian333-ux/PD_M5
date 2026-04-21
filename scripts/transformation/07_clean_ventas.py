from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_SALES_PATH = Path("data/raw/sales_raw.csv")
PROCESSED_VENTAS_PATH = Path("data/processed/ventas_clean.csv")


def clean_ventas(
    input_path: Path = RAW_SALES_PATH,
    output_path: Path = PROCESSED_VENTAS_PATH,
) -> pd.DataFrame:
    """Clean and transform the sales dataset."""
    # Load raw sales data
    df = pd.read_csv(input_path)

    # Report nulls before cleaning
    print("=== Nulls Report Before Cleaning ===")
    print(df.isnull().sum())
    print()

    # Convert ORDERDATE to datetime
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')

    # Remove duplicates
    initial_shape = df.shape
    df = df.drop_duplicates()
    print(f"Removed {initial_shape[0] - df.shape[0]} duplicate rows")

    # Select only relevant columns
    relevant_columns = [
        'ORDERNUMBER', 'ORDERDATE', 'PRODUCTCODE', 'QUANTITYORDERED', 'PRICEEACH', 'SALES', 'COUNTRY'
    ]
    df = df[relevant_columns]

    # Rename columns to snake_case
    column_mapping = {
        'ORDERNUMBER': 'order_number',
        'ORDERDATE': 'order_date',
        'PRODUCTCODE': 'product_code',
        'QUANTITYORDERED': 'quantity',
        'PRICEEACH': 'price',
        'SALES': 'sales',
        'COUNTRY': 'country'
    }
    df = df.rename(columns=column_mapping)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    df.to_csv(output_path, index=False)

    return df


def run() -> pd.DataFrame:
    """Execute the sales cleaning step."""
    df = clean_ventas()
    print("=== Ventas Clean Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nDtypes:")
    print(df.dtypes)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(5).to_string(index=False))
    print(f"\nArchivo procesado guardado en: {PROCESSED_VENTAS_PATH}")
    return df


if __name__ == "__main__":
    run()