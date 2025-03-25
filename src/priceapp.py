import pickle
import numpy as np
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Cargar el modelo
model_path = '/workspaces/MLWEB-FLASK/models/Price_model_flask.sav'
with open(model_path, 'rb') as file:
    modelo = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html', 
                           marcas=['Toyota', 'Chevrolet', 'Ford', 'Honda', 'Nissan'],
                           modelos=['Altima', 'Camry', 'Silverado', 'F-150', 'Civic'],
                           anos=list(range(2010, 2023)),
                           estados=['Excellent', 'Good', 'Fair'])

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        marca = data.get('Marca')
        modelo_auto = data.get('Modelo')
        ano = int(data.get('Ano'))
        kilometraje = float(data.get('Kilometraje'))
        estado = data.get('Estado')

        # Validaciones
        if marca not in ['Toyota', 'Chevrolet', 'Ford', 'Honda', 'Nissan']:
            return jsonify({'error': 'Marca inválida'})
        if modelo_auto not in ['Altima', 'Camry', 'Silverado', 'F-150', 'Civic']:
            return jsonify({'error': 'Modelo inválido'})
        if ano < 2010 or ano > 2022:
            return jsonify({'error': 'Año fuera de rango'})
        if kilometraje < 10000 or kilometraje > 150000:
            return jsonify({'error': 'Kilometraje fuera de rango'})
        if estado not in ['Excellent', 'Good', 'Fair']:
            return jsonify({'error': 'Estado inválido'})

        # Transformación de entrada
        entrada = np.array([[marca, modelo_auto, ano, kilometraje, estado]])
        precio_predicho = modelo.predict(entrada)[0]

        return jsonify({'precio_predicho': precio_predicho})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)