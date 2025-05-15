from flask import Flask

from predictor.src.app import create_app
from shared.config import Config


class DummyConfig(Config):
    DEBUG = True
    TESTING = True
    CUSTOM_VALUE = "test"


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
