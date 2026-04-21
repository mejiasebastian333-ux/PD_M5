from scripts.ingestion.01_load_sales import run as load_sales
from scripts.ingestion.02_fetch_clientes import run as fetch_clientes
from scripts.ingestion.03_fetch_regiones import run as fetch_regiones
from scripts.transformation.04_clean_ventas import run as clean_ventas
from scripts.transformation.05_build_productos import run as build_productos
from scripts.transformation.06_clean_clientes import run as clean_clientes
from scripts.transformation.07_enrich_regiones import run as enrich_regiones
from scripts.integration.08_integrate_master import run as integrate_master
from db.init_db import init_db
from scripts.db.09_load_to_postgres import run as load_to_postgres
from scripts.analysis.10_eda import run as perform_eda
from scripts.analysis.11_analisis_negocio import run as analisis_negocio
from scripts.analysis.12_sql_queries import run as sql_queries
from scripts.visualization.13_prepare_powerbi import run as prepare_powerbi

# Pipeline end-to-end
def run_pipeline():
    print("Iniciando pipeline...")
    # Fase 1: Ingesta
    load_sales()
    fetch_clientes()
    fetch_regiones()
    # Fase 2: Transformación
    clean_ventas()
    build_productos()
    clean_clientes()
    enrich_regiones()
    # Fase 3: Integración
    integrate_master()
    # Fase 4: Carga a DB
    init_db()
    load_to_postgres()
    # Fase 5: Análisis
    perform_eda()
    analisis_negocio()
    sql_queries()
    # Fase 6: Preparación para Power BI
    prepare_powerbi()
    print("Pipeline completado.")

if __name__ == "__main__":
    run_pipeline()