from typing import TYPE_CHECKING

from flask import Flask

from data_ingest.src import routes as _  # noqa: F401
from data_ingest.src.blueprint import home_bp, ingestor_bp

if TYPE_CHECKING:
    from shared.config import Config


def create_app(config: "Config") -> Flask:
    """
    Create a Flask application instance with the specified configuration.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["CONFIG"] = config

    # Mounts the blueprint to the app
    app.register_blueprint(home_bp)
    app.register_blueprint(ingestor_bp, url_prefix="/ingestor")

    print("\n[DEBUG] Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} -> {rule.rule}")

    return app


__all__ = ["create_app"]
