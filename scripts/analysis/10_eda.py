from __future__ import annotations

from pathlib import Path

import pandas as pd
from db.connection import get_connection, release_connection

DOCS_DIR = Path("docs")

def perform_eda() -> None:
    """Realiza análisis exploratorio usando SQL en PostgreSQL."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Estadísticas descriptivas
        cursor.execute("SELECT COUNT(*), AVG(sales), SUM(sales) FROM fact_ventas;")
        stats = cursor.fetchone()
        print(f"Total registros: {stats[0]}, Promedio ventas: {stats[1]}, Total ventas: {stats[2]}")

        # Distribución de ventas por país
        df_country = pd.read_sql("SELECT country, COUNT(*) as orders, SUM(sales) as total_sales FROM fact_ventas GROUP BY country ORDER BY total_sales DESC;", conn)
        print("Top países por ventas:")
        print(df_country.head())

        # Evolución mensual
        df_monthly = pd.read_sql("SELECT DATE_TRUNC('month', order_date) as month, SUM(sales) as total_sales FROM fact_ventas GROUP BY month ORDER BY month;", conn)
        print("Evolución mensual de ventas:")
        print(df_monthly)

        # Guardar reporte
        with open(DOCS_DIR / "eda_reporte.md", "w") as f:
            f.write("# EDA Reporte\n\n")
            f.write(f"Total registros: {stats[0]}\n")
            f.write(f"Promedio ventas: {stats[1]}\n")
            f.write(f"Total ventas: {stats[2]}\n\n")
            f.write("Top países:\n")
            f.write(df_country.to_markdown())
            f.write("\n\nEvolución mensual:\n")
            f.write(df_monthly.to_markdown())

        print("EDA completado. Reporte en docs/eda_reporte.md")

    except Exception as e:
        print(f"Error en EDA: {e}")
    finally:
        release_connection(conn)

def run() -> None:
    """Ejecuta el EDA."""
    perform_eda()

if __name__ == "__main__":
    run()