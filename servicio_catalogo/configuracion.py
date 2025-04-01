import requests
import os


CONFIG_URL = "http://localhost:5001/configuracion"

def obtener_configuracion():
    try:
        respuesta = requests.get(CONFIG_URL)
        if respuesta.status_code == 200:
            configuracion = respuesta.json()
            
            # 🔹 Agregamos los datos de MySQL si es el servicio de catálogo
            if "servicio_catalogo" in configuracion:
                configuracion["servicio_catalogo"]["MYSQL"] = {
                    "host": "127.0.0.1",
                    "user": "root",
                    "password": "",
                    "database": "catalogo_bd"
                }
            return configuracion
        else:
            raise Exception("Error al obtener la configuración")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return {}
