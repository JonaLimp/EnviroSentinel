from unittest.mock import patch

import pytest

from data_ingest.config import load_config
from data_ingest.src.app import create_app


@pytest.fixture
def client():
    config = load_config()
    app = create_app(config)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("data_ingest.src.routes.PredictorSender.send")
@patch("data_ingest.src.routes.OpenSenseFetcher.fetch_latest")
def test_ingest_success(mock_fetch, mock_send, client):
    mock_fetch.return_value = {
        "Temperature": {
            "value": 21.5,
            "unit": "°C",
            "timestamp": "2024-01-01T00:00:00Z",
        }
    }
    mock_send.return_value = {"anomaly": False}

    response = client.get("/ingestor/ingest")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    expected_len = len(client.application.config["CONFIG"].BOX_IDS)
    assert len(data) == expected_len

    for entry in data:
        assert "box_id" in entry
        assert "box_name" in entry
        assert "data" in entry
        assert "prediction" in entry


@patch(
    "data_ingest.src.routes.PredictorSender.send",
    side_effect=Exception("Prediction failed"),
)
@patch("data_ingest.src.routes.OpenSenseFetcher.fetch_latest")
def test_ingest_with_prediction_error(mock_fetch, mock_send, client):
    mock_fetch.return_value = {
        "Humidity": {"value": 50.0, "unit": "%", "timestamp": "2024-01-01T00:00:00Z"}
    }

    response = client.get("/ingestor/ingest")
    assert response.status_code == 200
    data = response.get_json()
    print("DEBUG ingest response (error test):", data)

    assert isinstance(data, list)
    assert any("error" in entry for entry in data)


def test_ingest_route_success(client):
    with (
        patch(
            "data_ingest.src.routes.PredictorSender.send",
            return_value={"anomaly": False},
        ),
        patch(
            "data_ingest.src.routes.OpenSenseFetcher.fetch_latest",
            return_value={
                "Temperature": {
                    "value": 22.1,
                    "unit": "°C",
                    "timestamp": "2024-01-01T00:00:00Z",
                }
            },
        ),
        patch("data_ingest.src.routes.OpenSenseFetcher.__init__", return_value=None),
    ):
        response = client.get("/ingestor/ingest")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert all("data" in item and "prediction" in item for item in data)
