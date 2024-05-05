# server.py

from flask import Flask, request, jsonify
from machine_learning_logic import machine_learning_logic
from machine_learning_logic_grupos import machine_learning_logic_grupos

app = Flask(__name__)

@app.route('/recomendar', methods=['POST'])
def recomendar_peliculas():
    data = request.get_json()
    usuario_en = data.get('usuario_en', [])
    
    # Llamar a la función de machine learning
    recomendaciones = machine_learning_logic(usuario_en)
    
    # Resto del código...
    return recomendaciones

@app.route('/recomendarGrupos', methods=['POST'])
def recomendar_grupos():
    data = request.get_json()
    usuario_en = data.get('usuario_en', [])
    
    # Llamar a la función de machine learning
    recomendaciones = machine_learning_logic_grupos(usuario_en)
    
    # Resto del código...
    return recomendaciones

if __name__ == '__main__':
    app.run(debug=True)
