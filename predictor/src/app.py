from typing import TYPE_CHECKING

from flask import Flask

from predictor.logger import get_logger
from predictor.src import routes  # noqa: F401
from predictor.src.blueprint import home_bp, predictor_bp

if TYPE_CHECKING:
    from predictor.config import Config

logger = get_logger(__name__)


def create_app(config: "Config") -> Flask:
    """
    Create a Flask application instance with the specified configuration.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    logger.info("Loaded Config:")
    for key in vars(config):
        logger.info(f"{key} = {getattr(config, key)}")

    app.register_blueprint(home_bp)
    app.register_blueprint(predictor_bp, url_prefix="/predictor")

    print("\n[DEBUG] Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} -> {rule.rule}")

    return app


__all__ = ["create_app"]
