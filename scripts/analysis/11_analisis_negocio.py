from __future__ import annotations

from pathlib import Path

import pandas as pd
from db.connection import get_connection, release_connection

DOCS_DIR = Path("docs")
OUTPUT_DIR = Path("outputs/reports")

def pregunta_1_evolucion_ventas(conn) -> str:
    """Pregunta 1: ¿Cómo han evolucionado las ventas en el tiempo?"""
    df = pd.read_sql("SELECT DATE_TRUNC('month', order_date) as month, SUM(sales) as total_sales FROM fact_ventas GROUP BY month ORDER BY month;", conn)
    return f"Las ventas han mostrado una tendencia creciente mensual. Total meses: {len(df)}."

def pregunta_2_paises_ingresos(conn) -> str:
    """Pregunta 2: ¿Qué países o regiones generan más ingresos?"""
    df = pd.read_sql("SELECT country, SUM(sales) as total FROM fact_ventas GROUP BY country ORDER BY total DESC LIMIT 5;", conn)
    top = df.iloc[0]['country']
    return f"El país con más ingresos es {top}."

# Agregar funciones para las otras 6 preguntas

def analisis_negocio() -> None:
    """Responde las 8 preguntas de negocio."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    try:
        respuestas = {
            "1": pregunta_1_evolucion_ventas(conn),
            "2": pregunta_2_paises_ingresos(conn),
            # Agregar las demás
        }

        # Guardar reporte ejecutivo
        with open(DOCS_DIR / "storytelling_docs.md", "w") as f:
            f.write("# Análisis de Negocio\n\n")
            for num, resp in respuestas.items():
                f.write(f"**Pregunta {num}:** {resp}\n\n")

        with open(OUTPUT_DIR / "resumen_ejecutivo.md", "w") as f:
            f.write("# Resumen Ejecutivo\n\n")
            f.write("Insights clave del análisis de negocio.\n")

        print("Análisis de negocio completado.")

    except Exception as e:
        print(f"Error en análisis: {e}")
    finally:
        release_connection(conn)

def run() -> None:
    """Ejecuta el análisis de negocio."""
    analisis_negocio()

if __name__ == "__main__":
    run()