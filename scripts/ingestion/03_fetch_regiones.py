from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests


API_URL = "https://api.first.org/data/v1/countries"
RAW_JSON_OUTPUT_PATH = Path("data/raw/regiones_raw.json")
RAW_CSV_OUTPUT_PATH = Path("data/raw/regiones_raw.csv")


def _save_json(payload: list[dict], output_path: Path) -> None:
    """Persist the untouched API response as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def _print_observation_report(df: pd.DataFrame) -> None:
    """Print a quick exploratory report for the raw regiones dataset."""
    print("=== Regiones Raw Dataset Report ===")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head(3).to_string(index=False))


def fetch_regiones(
    api_url: str = API_URL,
    json_output_path: Path = RAW_JSON_OUTPUT_PATH,
    csv_output_path: Path = RAW_CSV_OUTPUT_PATH,
) -> pd.DataFrame:
    """Fetch the regiones API response and persist untouched raw artifacts."""
    response = requests.get(api_url, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(
            f"Error consultando la API de regiones. "
            f"Status code recibido: {response.status_code}"
        )

    data = response.json()
    payload = data["data"]  # dict of countries

    # Convert to list of dicts
    countries_list = []
    for code, info in payload.items():
        countries_list.append({
            "code": code,
            "name.common": info["country"],
            "region": info["region"]
        })

    df = pd.DataFrame(countries_list)

    _save_json(countries_list, json_output_path)
    csv_output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_output_path, index=False)
    return df


def run() -> pd.DataFrame:
    """Execute the raw regiones ingestion step."""
    df = fetch_regiones()
    _print_observation_report(df)
    print(f"\nArchivo raw JSON generado en: {RAW_JSON_OUTPUT_PATH}")
    print(f"Archivo raw CSV generado en: {RAW_CSV_OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    run()
