# Ejecutar desde cd IA -> python -m api.app


from flask import Flask, request, jsonify
from flask_cors import CORS
from IA.sistema_experto.riskModel import predict_risk

app = Flask(__name__)

# Habilitar CORS para todas las rutas y orígenes
CORS(app)

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json
    historial = predict_risk(data)
    return jsonify({ "historial": historial })

if __name__ == "__main__":
    app.run(debug=True)