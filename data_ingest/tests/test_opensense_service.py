from unittest.mock import Mock, patch

import pytest

from data_ingest.src.opensense_service import OpenSenseFetcher


@pytest.fixture
def fetcher():
    return OpenSenseFetcher("https://api.opensensemap.org/boxes")


def mock_response(json_data, status_code=200):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status = Mock()
    return mock_resp


@patch("requests.get")
def test_fetch_latest_success(mock_get, fetcher):
    box_id = "abc123"
    mock_data = {
        "sensors": [
            {
                "title": "Temperature",
                "unit": "°C",
                "lastMeasurement": {
                    "value": "22.5",
                    "createdAt": "2024-01-01T12:00:00Z",
                },
            }
        ]
    }

    mock_get.return_value = mock_response(mock_data)

    result = fetcher.fetch_latest(box_id)

    assert isinstance(result, dict)
    assert "Temperature" in result
    assert result["Temperature"]["value"] == 22.5
    assert result["Temperature"]["unit"] == "°C"
    assert result["Temperature"]["timestamp"] == "2024-01-01T12:00:00Z"


@patch("requests.get")
def test_fetch_data_filters_invalid_sensor(mock_get):
    url = "https://api.opensensemap.org/boxes/abc123"

    # sensor value is not floatable
    mock_get.return_value = mock_response(
        {
            "sensors": [
                {
                    "title": "Noise",
                    "unit": "dB",
                    "lastMeasurement": {
                        "value": "not_a_number",
                        "createdAt": "2024-01-01T00:00:00Z",
                    },
                }
            ]
        }
    )

    result = OpenSenseFetcher._fetch_data(url, ["Temperature"])
    assert result == {}  # Should skip due to invalid float
