from typing import Literal

from flask import Response, jsonify, request

from predictor.config import load_config
from predictor.src.blueprint import predictor_bp
from predictor.src.model_service import Predictor
from predictor.src.preprocessor import Preprocessor

config = load_config()

preprocessor = Preprocessor(
    False, config.SOUND_ENCODER_PATH, config.STATION_ENCODER_PATH, history_size=10
)
predictor = Predictor(config)


@predictor_bp.route("/predict", methods=["POST"])
def predict_endpoint() -> tuple[Response, Literal[400]] | Response:
    payload = request.get_json()
    if not payload or "data" not in payload or "box_name" not in payload:
        return jsonify({"error": "Missing 'data' or 'box_name' in request"}), 400

    box_name = payload["box_name"]
    sensor_data = payload["data"]

    try:
        features = preprocessor.transform_from_sensor_data(sensor_data, box_name)

        result = predictor.predict([features])
        return jsonify({"predictions": result.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


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
