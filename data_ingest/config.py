import json
import os
from dataclasses import dataclass
from pathlib import Path

from shared.config import Config


@dataclass
class DataIngestConfig(Config):
    DATA_INGEST_URL: str
    PREDICTOR_URL: str
    BASE_URL: str
    SENSOR_CONFIG_PATH: Path
    BOX_IDS: dict[str, str]
    SENSOR_TYPES: dict[str, list[str]]
    PROJECT_ROOT: Path
    DEBUG: bool = True
    TESTING: bool = False
    FLASK_ENV: str = "development"


def load_data_ingest_config() -> DataIngestConfig:
    root = Path(__file__).parent.parent
    config_path = root / os.getenv("SENSOR_CONFIG_PATH", "sensor_config.json")

    try:
        with open(config_path) as f:
            sensor_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load sensor config from {config_path}: {e}")

    return DataIngestConfig(
        DATA_INGEST_URL=os.getenv("DATA_INGEST_URL", "http://localhost:5000"),
        PREDICTOR_URL=os.getenv("PREDICTOR_URL", "http://localhost:5001"),
        BASE_URL=os.getenv("BASE_URL", "https://api.opensensemap.org/boxes"),
        SENSOR_CONFIG_PATH=config_path,
        BOX_IDS=sensor_data["boxes"],
        SENSOR_TYPES=sensor_data["sensor_types"],
        PROJECT_ROOT=root,
    )
