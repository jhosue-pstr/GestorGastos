from flask import Flask, render_template, request, redirect, url_for
import categorias  # Módulo para manejar categorías
import py_eureka_client.eureka_client as eureka_client
import time
import threading

app = Flask(__name__)

# Configuración de Eureka
eureka_server = "http://localhost:9000/eureka"  
app_name = "servicio_categoria"  
instance_port = 5007  

eureka_client.init(eureka_server=eureka_server,
                   app_name=app_name,
                   instance_port=instance_port)

def send_heartbeat():
    """Envía un heartbeat cada 30 segundos para renovar la instancia en Eureka."""
    while True:
        eureka_client.renew("servicio_categoria") 
        print("Heartbeat enviado.")
        time.sleep(30) 

heartbeat_thread = threading.Thread(target=send_heartbeat)
heartbeat_thread.daemon = True
heartbeat_thread.start()

# Rutas del servicio
@app.route("/", methods=["GET", "POST"])
def index():
    lista_categorias = categorias.obtener_categorias()
    return render_template("index.html", categorias=lista_categorias)

@app.route("/buscar-categoria", methods=["POST"])
def buscar_categoria():
    search = request.form["buscar"]
    lista_categorias = categorias.buscar_categorias(search)
    return render_template("busqueda.html", categorias=lista_categorias, busqueda=search)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    categorias.agregar_categoria(nombre)
    return redirect(url_for("index"))

@app.route("/eliminar/<int:id>")
def eliminar(id):
    categorias.eliminar_categoria(id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5007)
