from flask import Flask, render_template, request, redirect, url_for
import productos
import time
from configuracion import *

app = Flask(__name__)

@app.route("/", methods= ["GET" , "POST"])
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
