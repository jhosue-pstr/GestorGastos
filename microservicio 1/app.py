from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

INFO = {
    "lenguajes": ["Python", "Java", "JavaScript", "C#", "PHP"],
    "frameworks": ["Flask", "Spring", "NodeJS", ".NET", "Laravel"],
    "bases": ["React", "Angular", "Vue", "Django", "Ruby on Rails"]
}

@app.route('/')
def index():
    return render_template('index.html', datos=INFO)



# Obtener toda la información en formato JSON
@app.route("/json", methods=['GET'])
def obtener_json():
    return make_response(jsonify(INFO), 200)



# Obtener todas las categorías disponibles
@app.route("/categorias", methods=['GET'])
def obtener_categorias():
    return jsonify({"categorias": list(INFO.keys())})



# Obtener una categoría específica
@app.route("/categoria/<string:categoria>", methods=['GET'])
def obtener_categoria(categoria):
    if categoria in INFO:
        return jsonify({categoria: INFO[categoria]})
    return jsonify({"error": "Categoría no encontrada"}), 404



# Agregar un nuevo elemento a una categoría
@app.route("/categoria/<string:categoria>/agregar", methods=['POST'])
def agregar_elemento(categoria):
    if categoria in INFO:
        data = request.get_json()
        nuevo_elemento = data.get("elemento")
        if nuevo_elemento:
            INFO[categoria].append(nuevo_elemento)
            return jsonify({"mensaje": f"{nuevo_elemento} agregado a {categoria}", categoria: INFO[categoria]})
        return jsonify({"error": "Falta el campo 'elemento' en el JSON"}), 400
    return jsonify({"error": "Categoría no encontrada"}), 404



# Actualizar un elemento en una categoría
@app.route("/categoria/<string:categoria>/actualizar", methods=['PUT'])
def actualizar_elemento(categoria):
    if categoria in INFO:
        data = request.get_json()
        elemento_antiguo = data.get("elemento_antiguo")
        elemento_nuevo = data.get("elemento_nuevo")
        
        if elemento_antiguo in INFO[categoria]:
            index = INFO[categoria].index(elemento_antiguo)
            INFO[categoria][index] = elemento_nuevo
            return jsonify({"mensaje": f"{elemento_antiguo} actualizado a {elemento_nuevo} en {categoria}", categoria: INFO[categoria]})
        
        return jsonify({"error": f"'{elemento_antiguo}' no encontrado en {categoria}"}), 404
    return jsonify({"error": "Categoría no encontrada"}), 404



# Eliminar un elemento de una categoría
@app.route("/categoria/<string:categoria>/eliminar", methods=['DELETE'])
def eliminar_elemento(categoria):
    if categoria in INFO:
        data = request.get_json()
        elemento = data.get("elemento")
        if elemento in INFO[categoria]:
            INFO[categoria].remove(elemento)
            return jsonify({"mensaje": f"{elemento} eliminado de {categoria}", categoria: INFO[categoria]})
        return jsonify({"error": f"'{elemento}' no encontrado en {categoria}"}), 404
    return jsonify({"error": "Categoría no encontrada"}), 404



# Eliminar una categoría completa
@app.route("/categoria/<string:categoria>", methods=['DELETE'])
def eliminar_categoria(categoria):
    if categoria in INFO:
        del INFO[categoria]
        return jsonify({"mensaje": f"Categoría {categoria} eliminada"})
    return jsonify({"error": "Categoría no encontrada"}), 404




# Crear una nueva categoría con elementos iniciales
@app.route("/categoria/agregar", methods=['POST'])
def agregar_categoria():
    data = request.get_json()
    nueva_categoria = data.get("categoria")
    elementos = data.get("elementos", [])

    if nueva_categoria in INFO:
        return jsonify({"error": "La categoría ya existe"}), 400
    
    INFO[nueva_categoria] = elementos
    return jsonify({"mensaje": f"Categoría {nueva_categoria} agregada", "INFO": INFO})



# Buscar un elemento en todas las categorías
@app.route("/buscar", methods=['GET'])
def buscar_elemento():
    query = request.args.get("query", "").lower()
    resultados = {}

    for categoria, elementos in INFO.items():
        coincidencias = [item for item in elementos if query in item.lower()]
        if coincidencias:
            resultados[categoria] = coincidencias

    if resultados:
        return jsonify(resultados)
    
    return jsonify({"mensaje": "No se encontraron coincidencias"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
