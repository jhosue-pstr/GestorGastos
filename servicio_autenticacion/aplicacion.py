from flask import Flask, jsonify
import configuracion

app = Flask(__name__)

# Obtener configuración desde el servicio centralizado
config = configuracion.obtener_configuracion()["servicio_autenticacion"]

@app.route('/')
def home():
    return jsonify({"mensaje": config["MENSAJE_BIENVENIDA"]})

if __name__ == '__main__':
    app.run(port=config["PUERTO"], debug=True)
