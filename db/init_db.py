from db.connection import get_connection, release_connection

def init_db():
    """Inicializa la base de datos creando tablas si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Leer el schema.sql
        with open('sql/schema.sql', 'r') as f:
            schema_sql = f.read()

        # Ejecutar el schema
        cursor.execute(schema_sql)
        conn.commit()
        print("Tablas creadas exitosamente en PostgreSQL.")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        conn.rollback()
    finally:
        release_connection(conn)

if __name__ == "__main__":
    init_db()