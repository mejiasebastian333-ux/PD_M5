from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_INPUT_PATH = Path("data/raw/sales_data_sample.csv")
RAW_OUTPUT_PATH = Path("data/raw/sales_raw.csv")


def _read_sales_csv(csv_path: Path) -> pd.DataFrame:
    """Read the source CSV without transformations."""
    try:
        return pd.read_csv(csv_path)
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding="latin-1")


def _print_observation_report(df: pd.DataFrame) -> None:
    """Print a quick exploratory report for the raw dataset."""
    print("=== Sales Raw Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nDtypes:")
    print(df.dtypes)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(5).to_string(index=False))
    print("\nNulls by column:")
    print(df.isnull().sum())


def load_sales(
    input_path: Path = RAW_INPUT_PATH,
    output_path: Path = RAW_OUTPUT_PATH,
) -> pd.DataFrame:
    """Load the sales CSV as-is and persist an untouched raw copy."""
    if not input_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de ventas en {input_path}. "
            "Descargalo y copialo antes de ejecutar este script."
        )

    df = _read_sales_csv(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def run() -> pd.DataFrame:
    """Execute the raw sales ingestion step."""
    df = load_sales()
    _print_observation_report(df)
    print(f"\nArchivo raw generado en: {RAW_OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    run()
