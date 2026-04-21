from __future__ import annotations

from pathlib import Path

import pandas as pd
from db.connection import get_connection, release_connection

OUTPUT_DIR = Path("outputs/exports")

def run_sql_queries() -> None:
    """Ejecuta las 8 queries de negocio en PostgreSQL y exporta resultados."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    queries = {
        "query_1_evolucion_ventas": """
        SELECT DATE_TRUNC('month', order_date) as month, SUM(sales) as total_sales
        FROM fact_ventas
        GROUP BY month
        ORDER BY month;
        """,
        "query_2_paises_ingresos": """
        SELECT country, SUM(sales) as total_sales
        FROM fact_ventas
        GROUP BY country
        ORDER BY total_sales DESC;
        """,
        "query_3_productos_desempeno": """
        SELECT producto_nombre, categoria, SUM(sales) as total_sales
        FROM fact_ventas
        GROUP BY producto_nombre, categoria
        ORDER BY total_sales DESC;
        """,
        # Agregar las otras 5 queries según las preguntas del PDF
    }

    conn = get_connection()
    try:
        for name, query in queries.items():
            df = pd.read_sql(query, conn)
            df.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
            print(f"Query {name} exportada.")
    except Exception as e:
        print(f"Error en queries: {e}")
    finally:
        release_connection(conn)

def run() -> None:
    """Ejecuta las queries SQL."""
    run_sql_queries()
    print("Queries SQL completadas.")

if __name__ == "__main__":
    run()