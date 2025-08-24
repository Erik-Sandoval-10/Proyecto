import mysql.connector

# Configuración de conexión a MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",       # 👈 cámbialo por tu usuario MySQL
    "password": "123456",  # 👈 cámbialo por tu contraseña MySQL
}

DB_NAME = "sgm"  # Nombre de la base de datos

# ---------- FUNCIÓN PRINCIPAL DE CONEXIÓN ----------
def get_connection():
    """
    Retorna una conexión a la base de datos 'sgm'.
    Si no existe la BD o las tablas, se crean automáticamente.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Crear la base de datos si no existe
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cursor.execute(f"USE {DB_NAME};")

    # Crear tablas si no existen
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(120) NOT NULL,
        telefono VARCHAR(50),
        email VARCHAR(120),
        direccion VARCHAR(200),
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT NOT NULL,
        marca VARCHAR(100),
        modelo VARCHAR(100),
        serie VARCHAR(100) UNIQUE,
        tipo VARCHAR(50),
        recibido_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tecnicos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(120) NOT NULL,
        email VARCHAR(120),
        telefono VARCHAR(50),
        activo TINYINT DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordenes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        equipo_id INT NOT NULL,
        tecnico_id INT NULL,
        tipo VARCHAR(20),
        descripcion VARCHAR(500),
        estado VARCHAR(20) DEFAULT 'Abierta',
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        cerrado_en TIMESTAMP NULL,
        FOREIGN KEY (equipo_id) REFERENCES equipos(id),
        FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    # Retornamos la conexión lista para consultas
    return mysql.connector.connect(database=DB_NAME, **DB_CONFIG)

# ---------- TEST AL EJECUTAR DIRECTO ----------
if __name__ == "__main__":
    conn = get_connection()
    print("✅ Base de datos y tablas listas en MySQL")
    conn.close()