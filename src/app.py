import pickle
import pandas as pd
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Load full pipeline
pipeline = pickle.load(open("../models/full_pipeline.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])
        prediction = pipeline.predict(input_df)[0]
        return jsonify({"Price": round(prediction, 2)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)