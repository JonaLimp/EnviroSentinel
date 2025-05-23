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


# --- Flat config object ---
class Config:
    # General
    PROJECT_ROOT = ROOT_DIR
    CONFIG_PATH = ENV_FILE
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    TESTING = os.getenv("TESTING", "false").lower() == "true"
    FLASK_ENV = os.getenv("FLASK_ENV", "production")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "")
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT", "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )

    # Model
    MODEL_PATH = PROJECT_ROOT / os.getenv("MODEL_PATH", "model/predictor_model.pkl")
    SCALER_PATH = PROJECT_ROOT / os.getenv("SCALER_PATH", "model/scaler.pkl")
    SOUND_ENCODER_PATH = PROJECT_ROOT / os.getenv(
        "SOUND_ENCODER_PATH", "model/sound_encoder.pkl"
    )
    STATION_ENCODER_PATH = PROJECT_ROOT / os.getenv(
        "STATION_ENCODER_PATH", "model/station_encoder.pkl"
    )
    ANOMALY_THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "0.7"))
    MODEL_NAME = MODEL_PATH.stem
    SCALER_NAME = SCALER_PATH.stem


def load_config():
    return Config
