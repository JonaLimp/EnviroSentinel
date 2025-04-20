from typing import TYPE_CHECKING, Generator
from unittest.mock import MagicMock, patch

import pytest
from flask import json

from src.app import create_app
from src.shared.config import load_config

if TYPE_CHECKING:
    from flask.testing import Flask, FlaskClient


@pytest.fixture
def app() -> Generator["Flask", None, None]:
    config = load_config("testing")
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
    sample_data = {"features": [12.0, 3.0]}

    dummy_result = MagicMock()
    dummy_result.tolist.return_value = [1]

    with patch("src.predictor.routes.predictor.predict", return_value=dummy_result):
        response = client.post(
            "/predictor/predict",
            data=json.dumps(sample_data),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.get_json() == {"predictions": [1]}


def test_predict_invalid_data(client: "FlaskClient") -> None:
    response = client.post(
        "/predictor/predict", data=json.dumps({}), content_type="application/json"
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid input data"
