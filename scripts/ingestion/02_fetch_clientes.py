from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests


API_URL = "https://randomuser.me/api/?results=100"
RAW_JSON_OUTPUT_PATH = Path("data/raw/clientes_raw.json")
RAW_CSV_OUTPUT_PATH = Path("data/raw/clientes_raw.csv")


def _save_json(payload: dict, output_path: Path) -> None:
    """Persist the untouched API response as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def _print_observation_report(df: pd.DataFrame) -> None:
    """Print a quick exploratory report for the raw clientes dataset."""
    print("=== Clientes Raw Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(3).to_string(index=False))


def fetch_clientes(
    api_url: str = API_URL,
    json_output_path: Path = RAW_JSON_OUTPUT_PATH,
    csv_output_path: Path = RAW_CSV_OUTPUT_PATH,
) -> pd.DataFrame:
    """Fetch the clientes API response and persist untouched raw artifacts."""
    response = requests.get(api_url, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(
            f"Error consultando la API de clientes. "
            f"Status code recibido: {response.status_code}"
        )

    payload = response.json()
    df = pd.json_normalize(payload["results"])

    _save_json(payload, json_output_path)
    csv_output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_output_path, index=False)
    return df


def run() -> pd.DataFrame:
    """Execute the raw clientes ingestion step."""
    df = fetch_clientes()
    _print_observation_report(df)
    print(f"\nArchivo raw JSON generado en: {RAW_JSON_OUTPUT_PATH}")
    print(f"Archivo raw CSV generado en: {RAW_CSV_OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    run()
