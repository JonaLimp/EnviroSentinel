from typing import Any, Dict

import requests


class OpenSenseFetcher:
    def __init__(self, url: str, allowed_sensor_types: Dict[str, str] = {}):
        self._url = url
        self._allowed_sensor_types = allowed_sensor_types

    def fetch_latest(self, box_id: str) -> Dict[str, Any]:
        url = f"{self._url}/{box_id}"
        print(f"url: {url}")
        print(f"allowed_sensor_types: {self._allowed_sensor_types}")
        try:
            results = self._fetch_data(
                url, allowed_sensor_types=self._allowed_sensor_types
            )
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            results = {}
        return results

    @staticmethod
    def _fetch_data(
        url: str, allowed_sensor_types: Dict[str, str] = {}
    ) -> Dict[str, Any]:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        result = {}
        for sensor in data.get("sensors", []):
            if sensor.get("title") not in allowed_sensor_types and allowed_sensor_types:
                continue
            try:
                result[sensor["title"]] = {
                    "value": float(sensor["lastMeasurement"]["value"]),
                    "unit": sensor["unit"],
                    "timestamp": sensor["lastMeasurement"]["createdAt"],
                }
            except (KeyError, ValueError, TypeError):
                continue
        return result
