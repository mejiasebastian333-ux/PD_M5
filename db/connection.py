import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool
from sqlalchemy import create_engine

# Cargar variables de entorno
load_dotenv()

# Configuración de PostgreSQL desde .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "emausoft_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Pool de conexiones psycopg2
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def get_connection():
    """Obtiene una conexión del pool."""
    return connection_pool.getconn()

def release_connection(conn):
    """Libera una conexión al pool."""
    connection_pool.putconn(conn)

# Engine de SQLAlchemy para pandas.to_sql
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

def test_connection():
    """Prueba la conexión a PostgreSQL."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Conexión exitosa: {version[0]}")
        release_connection(conn)
        return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False