from flask import Flask, render_template, request, redirect, url_for
import productos
import py_eureka_client.eureka_client as eureka_client
import time
import threading


app = Flask(__name__)







# Configuración de Eureka
eureka_server = "http://localhost:9000/eureka"  # URL de tu Eureka Server
app_name = "servicio_catalogo"  # Nombre de tu aplicación
instance_port = 5006  # El puerto donde tu microservicio Flask está corriendo

# Inicialización del cliente Eureka
eureka_client.init(eureka_server=eureka_server,
                   app_name=app_name,
                   instance_port=instance_port)

def send_heartbeat():
    """Envía un heartbeat cada 30 segundos para renovar la instancia."""
    while True:
        # Enviar un heartbeat para renovar la instancia registrada
        eureka_client.renew("servicio_catalogo")  # Este nombre debe coincidir con el registrado
        print("Heartbeat enviado.")
        time.sleep(30)  # Renovar cada 30 segundos

# Inicia el hilo de los heartbeats
heartbeat_thread = threading.Thread(target=send_heartbeat)
heartbeat_thread.daemon = True
heartbeat_thread.start()














@app.route("/", methods=["GET", "POST"])
def index():
    lista_productos = productos.obtener_productos()
    return render_template("index.html", productos=lista_productos)

@app.route("/buscar-producto", methods=["POST"])
def buscar_producto():
    search = request.form["buscar"]
    lista_productos = productos.buscar_productos(search)
    return render_template("busqueda.html", productos=lista_productos, busqueda=search)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    tipo = request.form["tipo"]
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    marca = request.form["marca"]
    fecha_ingreso = request.form["fecha_ingreso"]
    imagen_url = request.form["imagen_url"]
    productos.agregar_producto(nombre, precio, tipo, descripcion, cantidad, marca, fecha_ingreso, imagen_url)
    return redirect(url_for("index"))

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conexion = productos.conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5006) 
