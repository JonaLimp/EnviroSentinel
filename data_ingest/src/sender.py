import requests


class PredictorSender:
    def __init__(self, predictor_url: str):
        self.url = f"{predictor_url}/predictor/predict"

    def send(self, data: dict) -> dict:
        resp = requests.post(self.url, json=data)
        resp.raise_for_status()
        return resp.json()
