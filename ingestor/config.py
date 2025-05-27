import json
import os
from pathlib import Path

from dotenv import load_dotenv

# --- Load environment ---
SERVICE_DIR = Path(__file__).parent
ROOT_DIR = SERVICE_DIR.parent
ENV = os.getenv("ENV", "development")
ENV_FILE = SERVICE_DIR / f".env.{ENV}"

load_dotenv(SERVICE_DIR / ".env")
if ENV_FILE.exists():
    load_dotenv(ENV_FILE, override=True)
else:
    print(f"[WARN] {ENV_FILE} not found.")

# --- Load sensor config ---
SENSOR_CONFIG_PATH = ROOT_DIR / os.getenv("SENSOR_CONFIG_PATH", "sensor_config.json")
try:
    with open(SENSOR_CONFIG_PATH) as f:
        SENSOR_CONFIG = json.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load sensor config from {SENSOR_CONFIG_PATH}: {e}")


# --- Flat config object ---
class Config:
    # General
    PROJECT_ROOT = ROOT_DIR
    CONFIG_PATH = ENV_FILE
    PORT = int(os.getenv("PORT", 5001))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    TESTING = os.getenv("TESTING", "false").lower() == "true"
    FLASK_ENV = os.getenv("FLASK_ENV", "production")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "")
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT", "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )

    # Service
    DATA_INGEST_URL = os.getenv("DATA_INGEST_URL", "http://localhost:5000")
    PREDICTOR_URL = os.getenv("PREDICTOR_URL", "http://localhost:5001")
    BASE_URL = os.getenv("BASE_URL", "https://api.opensensemap.org/boxes")
    SENSOR_CONFIG_PATH = SENSOR_CONFIG_PATH
    BOX_IDS = SENSOR_CONFIG.get("boxes", {})
    SENSOR_TYPES = SENSOR_CONFIG.get("sensor_types", {})


def load_config():
    return Config()
