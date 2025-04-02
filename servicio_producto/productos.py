import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from configuracion import obtener_configuracion

config_db = obtener_configuracion()["servicio_producto"]["MYSQL"]

def conectar():
    return mysql.connector.connect(
        host=config_db["host"],
        user=config_db["user"],
        password=config_db["password"],
        database=config_db["database"]
    )




def buscar_productos(query):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    query = f"%{query}%"  
    cursor.execute("""
        SELECT * FROM productos
        WHERE nombre LIKE %s OR tipo LIKE %s OR marca LIKE %s
    """, (query, query, query))
    
    productos = cursor.fetchall()
    conexion.close()
    return productos





def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

def agregar_producto(nombre, precio, tipo, descripcion, cantidad, marca, fecha_ingreso, imagen_url):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, precio, tipo, descripcion, cantidad, marca, fecha_ingreso, imagen_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombre, precio, tipo, descripcion, cantidad, marca, fecha_ingreso, imagen_url))
    conexion.commit()
    conexion.close()
