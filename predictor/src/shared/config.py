import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from base .env file
load_dotenv(dotenv_path=".env", override=True)

# Load environment variables from specific .env file
env = os.getenv("ENV", "development")
load_dotenv(
    dotenv_path=f".env.{env}",
    override=True,
)


class Config:
    # Root directory of the project
    DEBUG = True
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    MODEL_PATH = PROJECT_ROOT / Path(os.getenv("MODEL_PATH", "model/default_model.pkl"))
    MODEL_NAME = MODEL_PATH.stem
    SCALER_PATH = PROJECT_ROOT / Path(
        os.getenv("SCALER_PATH", "model/default_scaler.pkl")
    )
    SCALER_NAME = SCALER_PATH.stem

    # Flask environment settings
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    PORT = int(os.getenv("PORT", 5001))

    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE = os.getenv("LOG_FILE", "")
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT", "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    ENV = "development"
    TESTING = False


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    FLASK_ENV = "testing"


CONFIG_MAP = {
    "production": ProductionConfig,
    "testing": TestingConfig,
    "development": DevelopmentConfig,
}


def load_config(env_name: str = "development") -> "Config":
    env = (env_name or os.getenv("ENV", "development")).lower()
    return CONFIG_MAP.get(env, DevelopmentConfig)()
