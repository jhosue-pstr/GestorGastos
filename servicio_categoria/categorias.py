import mysql.connector
from configuracion import obtener_configuracion

# Obtener configuración de la base de datos
config_db = obtener_configuracion().get("servicio_categoria", {}).get("MYSQL", {})

def conectar():
    """Conecta a la base de datos MySQL."""
    return mysql.connector.connect(
        host=config_db.get("host", "127.0.0.1"),
        user=config_db.get("user", "root"),
        password=config_db.get("password", ""),
        database=config_db.get("database", "categoria_db")
    )

def buscar_categorias(query):
    """Busca categorías en la base de datos según el nombre."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    query = f"%{query}%"
    cursor.execute("SELECT * FROM categorias WHERE nombre LIKE %s", (query,))
    categorias = cursor.fetchall()
    conexion.close()
    return categorias

def obtener_categorias():
    """Obtiene todas las categorías de la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    conexion.close()
    return categorias

def agregar_categoria(nombre):
    """Agrega una nueva categoría a la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
    conexion.commit()
    conexion.close()

def eliminar_categoria(id):
    """Elimina una categoría por ID."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()
