from __future__ import annotations

from pathlib import Path

import pandas as pd
from db.connection import engine, test_connection

MASTER_PATH = Path("data/integrated/emausoft_master.csv")

def load_master_to_postgres(csv_path: Path = MASTER_PATH) -> None:
    """Carga el dataset maestro a PostgreSQL."""
    # Probar conexión
    if not test_connection():
        raise RuntimeError("No se pudo conectar a PostgreSQL. Verifica las variables de entorno.")

    # Cargar CSV
    df = pd.read_csv(csv_path)

    # Cargar a PostgreSQL (reemplaza si existe)
    df.to_sql('fact_ventas', engine, if_exists='replace', index=False)
    print(f"Datos cargados a 'fact_ventas' desde {csv_path}.")

    # Nota: En un star schema real, dividir en dims y fact, pero para simplificar, todo en fact_ventas.

def run() -> None:
    """Ejecuta la carga a PostgreSQL."""
    load_master_to_postgres()
    print("Carga a PostgreSQL completada.")

if __name__ == "__main__":
    run()