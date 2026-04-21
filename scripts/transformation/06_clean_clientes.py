from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_CLIENTES_PATH = Path("data/raw/clientes_raw.csv")
PROCESSED_CLIENTES_PATH = Path("data/processed/clientes_clean.csv")


def clean_clientes(
    input_path: Path = RAW_CLIENTES_PATH,
    output_path: Path = PROCESSED_CLIENTES_PATH,
) -> pd.DataFrame:
    """Clean and structure the clientes dataset."""
    # Load raw clientes data
    df = pd.read_csv(input_path)

    # Select necessary fields
    df = df[['name.first', 'name.last', 'location.city', 'location.country']]

    # Create cliente_id autoincremental
    df['cliente_id'] = range(1, len(df) + 1)

    # Unify full name
    df['nombre'] = df['name.first'] + ' ' + df['name.last']

    # Rename columns
    df = df[['cliente_id', 'nombre', 'location.city', 'location.country']]
    df.columns = ['cliente_id', 'nombre', 'ciudad', 'pais']

    # Clean strings
    df['nombre'] = df['nombre'].str.strip()
    df['ciudad'] = df['ciudad'].str.strip()
    df['pais'] = df['pais'].str.strip()

    # Ensure cliente_id is unique and no nulls
    assert df['cliente_id'].is_unique, "cliente_id must be unique"
    assert df['cliente_id'].notnull().all(), "cliente_id cannot have nulls"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    df.to_csv(output_path, index=False)

    return df


def run() -> pd.DataFrame:
    """Execute the clientes cleaning step."""
    df = clean_clientes()
    print("=== Clientes Clean Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(5).to_string(index=False))
    print(f"\nArchivo procesado guardado en: {PROCESSED_CLIENTES_PATH}")
    return df


if __name__ == "__main__":
    run()