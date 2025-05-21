from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from numpy.typing import NDArray

from predictor.config import Config
from predictor.src.model_service import Predictor


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    ANOMALY_THRESHOLD = 0.9
    MODEL_PATH = Path("/tmp/test_model.pkl")
    SCALER_PATH = Path("/tmp/test_scaler.pkl")


@pytest.fixture
def mock_config() -> TestConfig:
    return TestConfig()


@pytest.fixture
def dummy_input() -> NDArray[np.float64]:
    return np.array([[1.0, 2.0], [3.0, 4.0]])


# Dummy model and scaler
class DummyModel:
    def predict(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.array([1, 0])


class DummyScaler:
    def transform(self, X: NDArray[np.float64]) -> NDArray[np.float64]:
        return X  # identity for testing


class TestPredictor:
    def test_predictor_predict(self, mock_config, dummy_input):
        with patch("predictor.src.model_service.joblib.load") as mock_load:
            # joblib.load gets called twice: once for model, once for scaler
            mock_load.side_effect = [DummyModel(), DummyScaler()]

            predictor = Predictor(mock_config)

            result = predictor.predict(dummy_input)

            assert isinstance(result, np.ndarray)
            assert list(result) == [1, 0]
            assert mock_load.call_count == 2
