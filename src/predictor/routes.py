from typing import Literal

from flask import Response, jsonify, request

from src.predictor.blueprint import predictor_bp
from src.predictor.model_service import Predictor
from src.shared.config import load_config

predictor = Predictor(load_config())


@predictor_bp.route("/predict", methods=["POST"])
def predict_endpoint() -> tuple[Response, Literal[400]] | Response:
    data = request.get_json()
    if not data or "features" not in data:
        return jsonify({"error": "Invalid input data"}), 400

    features = data.get("features", [])
    result = predictor.predict(features)
    return jsonify({"predictions": result.tolist()})


@predictor_bp.route("/health", methods=["GET"])
def health_endpoint() -> tuple[Response, Literal[200]]:
    """
    Health check endpoint to verify if the service is running.
    """
    return jsonify({"status": "healthy"}), 200


@predictor_bp.route("/", methods=["GET"])
def home() -> tuple[Response, Literal[200]]:
    """
    Home endpoint to verify if the service is running.
    """
    return jsonify(message=f"Welcome to Predictor at {predictor_bp.url_prefix} 👋"), 200
