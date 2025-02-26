from flask import Flask, request, render_template
from pickle import load

model = load(open("/workspace/MLWEB-FLASK/models/random_forest_regression_42.sav", "rb"))
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            year = float(request.form['Year'])
            engine_size = float(request.form['EngineSize'])
            mileage = float(request.form['Mileage'])
            owner_count = int(request.form['Owner_Count'])

            # Dummy prediction for testing
            prediction = year * engine_size - mileage / (owner_count + 1)

            return render_template('index.html', prediction=round(prediction, 2))
        except Exception as e:
            print(f"Error: {e}")
            return "Something went wrong", 500

    return render_template('index.html', prediction=0)
