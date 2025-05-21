from pathlib import Path

from flask import Flask

from predictor.config import Config
from predictor.src.app import create_app


class DummyConfig(Config):
    DEBUG: bool = True
    TESTING: bool = True
    CUSTOM_VALUE: str = "test"

    # Required base config values
    PORT: int = 5000
    PROJECT_ROOT: Path = Path("/tmp/project")
    FLASK_ENV: str = "development"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "stdout"
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
    CONFIG_PATH: Path = Path("/tmp/project/config.yml")

    # Predictor-specific values (if inherited from DataIngestConfig)
    DATA_INGEST_URL: str = "http://localhost:5001/fetch"
    PREDICTOR_URL: str = "http://localhost:5000/predictor/predict"
    BASE_URL: str = "https://api.opensensemap.org/boxes"
    SENSOR_CONFIG_PATH: Path = Path("/tmp/sensors.yml")
    BOX_IDS: dict[str, str] = {"box1": "123456"}
    SENSOR_TYPES: dict[str, list[str]] = {"temperature": ["°C"]}


def test_create_app_returns_flask_instance():
    app = create_app(DummyConfig())
    assert isinstance(app, Flask)
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True
    assert app.config["CUSTOM_VALUE"] == "test"


def test_create_app_registers_routes():
    app = create_app(DummyConfig())

    url_map = {rule.rule for rule in app.url_map.iter_rules()}

    assert "/" in url_map
    assert "/predictor/predict" in url_map
    assert "/predictor/health" in url_map
