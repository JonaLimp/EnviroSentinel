import os
from pathlib import Path


class BaseConfig:
    DEBUG: bool
    PROJECT_ROOT: Path
    FLASK_ENV: str
    PORT: int
    LOG_LEVEL: str
    LOG_FILE: str
    LOG_FORMAT: str
    ENV: str
    TESTING: bool

    # Predictor-specific
    MODEL_PATH: Path
    MODEL_NAME: str
    SCALER_PATH: Path
    SCALER_NAME: str
    ANOMALY_THRESHOLD: float


class Config(BaseConfig):
    DEBUG = True
    PROJECT_ROOT = Path(__file__).parent.parent
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    PORT = int(os.getenv("PORT", 5001))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE = os.getenv("LOG_FILE", "")
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT", "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )
    ENV = "base"
    TESTING = False


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = "development"


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    FLASK_ENV = "testing"


CONFIG_MAP: dict[str, type[Config]] = {
    "production": ProductionConfig,
    "testing": TestingConfig,
    "development": DevelopmentConfig,
}


def load_config() -> Config:
    env = os.getenv("ENV", "development")
    config_cls = CONFIG_MAP.get(env, DevelopmentConfig)
    return config_cls()
