import os
from dataclasses import dataclass
from pathlib import Path

from shared.config import Config


@dataclass
class PredictorConfig(Config):
    MODEL_PATH: Path
    MODEL_NAME: str
    SCALER_PATH: Path
    SCALER_NAME: str
    ANOMALY_THRESHOLD: float
    PROJECT_ROOT: Path
    DEBUG: bool = True
    TESTING: bool = False
    FLASK_ENV: str = "development"


def load_predictor_config() -> PredictorConfig:
    root = Path(__file__).parent.parent
    model_path = os.getenv("MODEL_PATH", "model/predictor_model.pkl")
    scaler_path = os.getenv("SCALER_PATH", "model/scaler.pkl")
    return PredictorConfig(
        MODEL_PATH=root / model_path,
        MODEL_NAME=Path(model_path).stem,
        SCALER_PATH=root / scaler_path,
        SCALER_NAME=Path(scaler_path).stem,
        ANOMALY_THRESHOLD=float(os.getenv("ANOMALY_THRESHOLD", "0.7")),
        PROJECT_ROOT=root,
    )
