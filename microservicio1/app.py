from flask import Flask, jsonify
import pymysql
import requests

app = Flask(__name__)

# Función para obtener la conexión a la base de datos
def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="microserv1"
    )

# Verificación de la conexión con el servicio config_service
CONFIG_SERVICE_URL = "http://config_service:5001/health"

try:
    response = requests.get(CONFIG_SERVICE_URL)
    print("✅ Conectado a config_service:", response.text)
except Exception as e:
    print("❌ Error al conectar a config_service:", str(e))

@app.route("/")
def home():
    return "Microservicio 1 conectado a config_service"

@app.route("/personas", methods=["GET"])
def obtener_personas():
    # Obtener conexión a la base de datos
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Consulta SQL para obtener todos los registros de la tabla personas
            cursor.execute("SELECT id, nombre, apellido, edad FROM personas")
            personas = cursor.fetchall()

            # Convertir los resultados en un formato JSON
            resultado = []
            for persona in personas:
                resultado.append({
                    "id": persona[0],
                    "nombre": persona[1],
                    "apellido": persona[2],
                    "edad": persona[3]
                })

            # Devolver los datos en formato JSON
            return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Cerrar la conexión
        conexion.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
