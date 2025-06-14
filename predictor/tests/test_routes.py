from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask, json
from flask.testing import FlaskClient

from predictor.config import load_config
from predictor.src.app import create_app


@pytest.fixture
def app() -> Generator["Flask", None, None]:
    config = load_config()
    app = create_app(config)
    app.testing = True
    yield app


@pytest.fixture
def client(app: Flask) -> "FlaskClient":
    return app.test_client()


def test_health_endpoint(client: "FlaskClient") -> None:
    response = client.get("/predictor/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_home_endpoint(client: "FlaskClient") -> None:
    response = client.get("/predictor/")
    assert response.status_code == 200
    assert "Welcome to Predictor" in response.get_json()["message"]


def test_predict_valid_data(client: "FlaskClient") -> None:
    sample_payload = {
        "box_name": "Schnus_Sense_Box",
        "data": {
            "Temperatur": {
                "value": 21.0,
                "unit": "°C",
                "timestamp": "2025-01-01T12:00:00Z",
            },
            "rel. Luftfeuchte": {
                "value": 50.0,
                "unit": "%",
                "timestamp": "2025-01-01T12:00:00Z",
            },
            "Lautstärke": {
                "value": 45.0,
                "unit": "dB",
                "timestamp": "2025-01-01T12:00:00Z",
            },
        },
    }

    dummy_result = MagicMock()
    dummy_result.tolist.return_value = [1]

    with patch("predictor.src.routes.predictor.predict", return_value=dummy_result):
        response = client.post(
            "/predictor/predict",
            data=json.dumps(sample_payload),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.get_json() == {"predictions": [1]}
