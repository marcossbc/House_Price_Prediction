from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
from Utilities import prepare_features_from_raw  # uses saved scaler + columns

# Initialize server
App = Flask(__name__)
CORS(App)

MODELS = {
    "lr": joblib.load("modeles/lr_model.joblib"),
    "rf": joblib.load("modeles/rf_model.joblib")
}

@App.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to House Price Prediction API",
        "endpoints": {
            "POST /predict?model=lr|rf": {
                "expects_json": {
                    "Size_m2": "float",
                    "Bedrooms": "int",
                    "Bathrooms": "int",
                    "YearBuilt": "int",
                    "Location": "City|Suburb|Rural"
                }
            }
        }
    })

@App.route("/predict", methods=["POST"])
def predict():
    # 1) choose model
    choice = request.args.get("model", "").lower()
    if choice not in MODELS:
        return jsonify({"error": "Unknown model. Use model=lr or model=rf"}), 400
    model = MODELS[choice]

    # 2) read payload
    data = request.get_json(silent=True) or {}
    required = ["Size_m2", "Bedrooms", "Bathrooms", "YearBuilt", "Location"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        x_new = prepare_features_from_raw(data)   # 1-row DataFrame
        pred = float(model.predict(x_new)[0])
    except Exception as e:
        return jsonify({"error": f"Failed to prepare/predict: {e}"}), 500

    return jsonify({
        "model": "linear_regression" if choice == "lr" else "random_forest",
        "input": {
            "Size_m2": float(data["Size_m2"]),
            "Bedrooms": int(data["Bedrooms"]),
            "Bathrooms": int(data["Bathrooms"]),
            "YearBuilt": int(data["YearBuilt"]),
            "Location": str(data["Location"])
        },
        "prediction": round(pred, 0)
    }) 



if __name__ == "__main__":
    App.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=True)
