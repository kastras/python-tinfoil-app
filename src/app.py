#python3
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import json_util

import json
app = Flask(__name__)

client = MongoClient(host="mongo") 
headers = {'accept': 'application/json'}


db = client['tinfoil']

collection = db['list']

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/save', methods=['POST'])
def guardar_dato():
    url = request.form.get('url')
    title = request.form.get('title')
    username = request.form.get('username')
    password = request.form.get('password')
    protocolo = request.form.get('protocol')
    puerto = request.form.get('puerto')
    path = request.form.get('path')

    if url and url :
        if username and password:
            username = f"{username}:"
        data = {'protocolo':protocolo,'url': url,'puerto': puerto, 'title':title,'username':username,'password':password,'path': path,"enabled":1}
        collection.insert_one(data)
        return jsonify({'message': 'Dato guardado correctamente'})
    else:
        return jsonify({'error': 'El dato no puede estar vacío'})

@app.route('/locations.json')
def mostrar_datos_en_json():
    # Consulta todos los documentos en la colección
    result = collection.find()
    # Convierte los documentos en una lista de diccionarios
    datos = list(result)
    datos = json.loads(json_util.dumps(datos))
    listaFinal = []
    for data in datos:
        del data['_id']

        if data['enabled']:
            if data['puerto']:
                data['puerto'] = f":{data['puerto']}"
            listaFinal.append(f"{data['protocolo']}://{data['username']}{data['password']}{data['url']}{data['puerto']}{data['path']}")
    final = {
        'locations' : listaFinal
    }
    return jsonify(final)


if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")
