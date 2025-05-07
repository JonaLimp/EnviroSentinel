from unittest.mock import patch

import numpy as np
import pytest
from numpy.typing import NDArray
from src.predictor.model_service import Predictor


class DummyConfig:
    MODEL_PATH = "model/mock_model.pkl"
    SCALER_PATH = "model/mock_scaler.pkl"
    MODEL_NAME = "mock_model"
    SCALER_NAME = "mock_scaler"


@pytest.fixture
def mock_config() -> DummyConfig:
    return DummyConfig()


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
        with patch("src.predictor.model_service.joblib.load") as mock_load:
            # joblib.load gets called twice: once for model, once for scaler
            mock_load.side_effect = [DummyModel(), DummyScaler()]

            predictor = Predictor(mock_config)

            result = predictor.predict(dummy_input)

            assert isinstance(result, np.ndarray)
            assert list(result) == [1, 0]
            assert mock_load.call_count == 2
