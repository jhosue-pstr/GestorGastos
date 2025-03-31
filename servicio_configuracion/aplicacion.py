from flask import Flask, jsonify
import json

app = Flask(__name__)

# Cargar la configuración desde el archivo JSON
with open("configuracion.json") as config_file:
    configuracion = json.load(config_file)

@app.route('/configuracion')
def obtener_configuracion():
    return jsonify(configuracion)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
