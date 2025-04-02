import requests

CONFIG_URL = "http://localhost:5001/configuracion"

def obtener_configuracion():
    try:
        respuesta = requests.get(CONFIG_URL)
        if respuesta.status_code == 200:
            configuracion = respuesta.json()
            
            # 🔹 Configuración de MySQL para el servicio de categorías
            if "servicio_categoria" in configuracion:
                configuracion["servicio_categoria"]["MYSQL"] = {
                    "host": "127.0.0.1",
                    "user": "root",
                    "password": "",
                    "database": "categoria_db"
                }
            return configuracion
        else:
            raise Exception("Error al obtener la configuración")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return {}
