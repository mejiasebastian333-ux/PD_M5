from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_REGIONES_PATH = Path("data/raw/regiones_raw.csv")
PROCESSED_REGIONES_PATH = Path("data/processed/regiones_clean.csv")


def enrich_regiones(
    input_path: Path = RAW_REGIONES_PATH,
    output_path: Path = PROCESSED_REGIONES_PATH,
) -> pd.DataFrame:
    """Clean and prepare the regiones dataset."""
    # Load raw regiones data
    df = pd.read_csv(input_path)

    # Select useful columns (note: new API doesn't have subregion)
    df = df[['name.common', 'region']]
    df['subregion'] = ''  # Add empty subregion for consistency

    # Rename columns
    df.columns = ['pais', 'region', 'subregion']

    # Remove rows with null or empty pais
    df = df[df['pais'].notnull() & (df['pais'] != '')]

    # Clean strings
    df['pais'] = df['pais'].str.strip()
    df['region'] = df['region'].str.strip()
    df['subregion'] = df['subregion'].str.strip()

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    df.to_csv(output_path, index=False)

    return df


def run() -> pd.DataFrame:
    """Execute the regiones cleaning step."""
    df = enrich_regiones()
    print("=== Regiones Clean Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(5).to_string(index=False))
    print(f"\nArchivo procesado guardado en: {PROCESSED_REGIONES_PATH}")
    return df


if __name__ == "__main__":
    run()