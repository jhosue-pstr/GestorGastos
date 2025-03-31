import requests

CONFIG_URL = "http://localhost:5001/configuracion"

def obtener_configuracion():
    respuesta = requests.get(CONFIG_URL)
    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        raise Exception("Error al obtener la configuración")
