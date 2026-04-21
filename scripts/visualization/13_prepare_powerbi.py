from __future__ import annotations

from pathlib import Path

import pandas as pd
from db.connection import get_connection, release_connection

OUTPUT_DIR = Path("outputs/exports")

def prepare_powerbi_exports() -> None:
    """Prepara exports de datos para Power BI desde PostgreSQL."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Export 1: Ventas por país y categoría
        query1 = """
        SELECT country, categoria, SUM(sales) as total_sales, COUNT(*) as num_orders
        FROM fact_ventas
        GROUP BY country, categoria
        ORDER BY total_sales DESC;
        """
        df1 = pd.read_sql(query1, conn)
        df1.to_csv(OUTPUT_DIR / "ventas_por_pais_categoria.csv", index=False)

        # Export 2: Evolución mensual de ventas
        query2 = """
        SELECT DATE_TRUNC('month', order_date) as month, SUM(sales) as total_sales
        FROM fact_ventas
        GROUP BY month
        ORDER BY month;
        """
        df2 = pd.read_sql(query2, conn)
        df2.to_csv(OUTPUT_DIR / "evolucion_ventas_mensual.csv", index=False)

        # Export 3: Top productos
        query3 = """
        SELECT producto_nombre, categoria, SUM(sales) as total_sales
        FROM fact_ventas
        GROUP BY producto_nombre, categoria
        ORDER BY total_sales DESC
        LIMIT 10;
        """
        df3 = pd.read_sql(query3, conn)
        df3.to_csv(OUTPUT_DIR / "top_productos.csv", index=False)

        print("Exports para Power BI generados en outputs/exports/")

    except Exception as e:
        print(f"Error al preparar exports: {e}")
    finally:
        release_connection(conn)

def run() -> None:
    """Ejecuta la preparación de datos para Power BI."""
    prepare_powerbi_exports()

if __name__ == "__main__":
    run()