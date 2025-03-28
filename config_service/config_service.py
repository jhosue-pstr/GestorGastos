from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    "host": "mysql_db",
    "user": "config_user",
    "password": "config_pass",
    "database": "config_db"
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Conectado a la base de datos de config_service:", cursor.fetchone())
except Exception as e:
    print("Error al conectar a MySQL en config_service:", str(e))

@app.route("/")
def home():
    return "Config Service conectado a MySQL"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
