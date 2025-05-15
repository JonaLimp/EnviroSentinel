import pytest

from data_ingest.src.opensense_service import OpenSenseFetcher


@pytest.fixture(scope="module")
def fetcher():
    base_url = "https://api.opensensemap.org/boxes"
    return OpenSenseFetcher(base_url)


def test_fetch_latest_integration(fetcher):
    box_id = "6595489a649ae60007d0fc04"  # real box ID from Berlin
    data = fetcher.fetch_latest(box_id)

    assert isinstance(data, dict)
    assert len(data) > 0

    for sensor_title, reading in data.items():
        assert "value" in reading
        assert "unit" in reading
        assert "timestamp" in reading
        assert isinstance(reading["value"], float)
        assert isinstance(reading["unit"], str)
        assert isinstance(reading["timestamp"], str)
