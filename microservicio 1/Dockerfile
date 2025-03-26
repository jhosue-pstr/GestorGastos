# Usa una imagen base de Python
FROM python:3.10.6

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . .

# Instala las dependencias necesarias
RUN pip install flask

# Expone el puerto 5000 (donde corre Flask)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
