from flask import Blueprint, Response, jsonify

predictor_bp = Blueprint("predictor", __name__)

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home() -> Response | str:
    return jsonify(message="Welcome to EnviroSentinel Prediction 👋")
