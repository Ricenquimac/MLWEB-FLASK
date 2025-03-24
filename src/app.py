from flask import Flask, request, render_template, flash
from pickle import load
import os

# Inicializar Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para flash messages

# Cargar el modelo
MODEL_PATH = "/workspace/MLWEB-FLASK/models/random_forest_regression_42.sav"

if os.path.exists(MODEL_PATH):
    model = load(open(MODEL_PATH, "rb"))
else:
    model = None
    print(f"Error: No se encontró el modelo en {MODEL_PATH}")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None

    if request.method == 'POST':
        try:
            if not model:
                flash("Modelo no cargado correctamente", "danger")
                return render_template('index.html', prediction=None)

            # Obtener valores del formulario
            year = float(request.form.get('Year', 0))
            engine_size = float(request.form.get('EngineSize', 0))
            mileage = float(request.form.get('Mileage', 0))
            owner_count = int(request.form.get('Owner_Count', 1))

            # Crear el array de entrada
            input_data = [[year, engine_size, mileage, owner_count]]

            # Hacer la predicción con el modelo
            prediction = model.predict(input_data)[0]

            flash("Predicción realizada con éxito", "success")

        except ValueError:
            flash("Error en la conversión de datos. Verifica los valores ingresados.", "danger")
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")

    return render_template('index.html', prediction=round(prediction, 2) if prediction is not None else None)