from typing import Generator

import pytest
from flask import Flask, json
from flask.testing import FlaskClient
from src.app import create_app
from src.shared.config import load_config


@pytest.fixture
def app() -> Generator["Flask", None, None]:
    config = load_config("testing")
    app = create_app(config)
    app.testing = True
    yield app


@pytest.fixture
def client(app: Flask) -> "FlaskClient":
    return app.test_client()


def test_predict_valid_data(client: "FlaskClient") -> None:
    sample_data = {
        "features": [
            [
                12.0,
                3.0,
                5.5,
                7.0,
                1.0,
                3.1,
                0.0,
                4.2,
                3.3,
                6.6,
                2.2,
                1.1,
                9.9,
                8.8,
                0.0,
                3.0,
                7.7,
                6.6,
                5.5,
            ]
        ]
    }

    response = client.post(
        "/predictor/predict",  # or "/predict" depending on registration
        data=json.dumps(sample_data),
        content_type="application/json",
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "predictions" in json_data
    assert isinstance(json_data["predictions"], list)
    assert json_data["predictions"][0] in [-1, 1]
