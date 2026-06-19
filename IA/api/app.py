import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from IA.sistema_experto.modelSUnificate import clinicPrediction, conductualPrediction, getMetricas

app = Flask(__name__)

# Habilitar CORS para todas las rutas y orígenes
CORS(app)

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json
    return jsonify({ "data": data })

@app.route("/api/clinic", methods=["POST"])
def predict_clinic():
    data = request.json
    clinic_result = clinicPrediction(data)
    return jsonify({ "clinic_result": clinic_result })

@app.route("/api/conductual", methods=["POST"])
def predict_conductual():
    data = request.json
    conductual_result = conductualPrediction(data)
    return jsonify({ "conductual_result": conductual_result })

@app.route("/api/metricas", methods=["POST"])
def get_metricas():
    data = request.json
    metricas_result = getMetricas(data)
    return jsonify({ "metricas_result": metricas_result })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)