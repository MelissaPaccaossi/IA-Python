# server.py

from flask import Flask, request, jsonify
from machine_learning_logic_grupos import machine_learning_logic_grupos, machine_learning_add_grupo

app = Flask(__name__)

@app.route('/recomendarGrupos', methods=['POST'])
def recomendar_grupos():
    data = request.get_json()
    usuario_en = data.get('usuario_en', [])
    preferencias_usuario = data.get('preferencias_usuario', {})
    
    # Llamar a la función de machine learning
    recomendaciones = machine_learning_logic_grupos(usuario_en, preferencias_usuario)
    
    return recomendaciones

@app.route('/agregarGrupo', methods=['POST'])
def agregar_grupo():
    data = request.get_json()
    nuevo_grupo = data.get('nuevo_grupo', {})
    
    # Llamar a la función de machine learning
    respuesta = machine_learning_add_grupo(nuevo_grupo)
    
    return respuesta

if __name__ == '__main__':
    app.run(debug=True)
