from typing import TYPE_CHECKING

import joblib

from src.shared.logger import get_logger

if TYPE_CHECKING:
    from numpy import ndarray
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler

    from src.shared.config import Config


class Predictor:
    def __init__(self, config: "Config") -> None:
        """
        Initialize the Predictor class.

        Parameters
        ----------
        config : Config
            A Config object containing the model and scaler paths.

        Attributes
        ----------
        model_name : str
            The name of the model.
        model_path : Path
            The path to the model file.
        scaler_name : str
            The name of the scaler.
        scaler_path : Path
            The path to the scaler file.
        model : object
            The loaded machine learning model.
        """
        self.logger = get_logger()
        self.model_name = config.MODEL_NAME
        self._model_path = config.MODEL_PATH
        self._scaler_path = config.SCALER_PATH
        self.scaler_name = config.SCALER_NAME

    def _load_scaler(self) -> "StandardScaler":
        """
        Load a scaler from the specified file path.

        Parameters
        ----------
        scaler_path : str
            The file path to load the scaler from.

        Returns
        -------
        object
            The loaded scaler.
        """
        self.logger.info(f"Loading {self.scaler_name} scaler...")
        scaler = joblib.load(self._scaler_path)
        return scaler

    def _load_model(self) -> "IsolationForest":
        """
        Load a machine learning model from the specified file path.

        Parameters
        ----------
        model_path : str
            The file path to load the model from.

        Returns
        -------
        object
            The loaded machine learning model.
        """
        self.logger.info(f"Loading {self.model_name}...")
        model = joblib.load(self._model_path)
        return model

    def predict(self, data: "ndarray") -> "ndarray":
        """
        Make predictions with the model.

        Parameters
        ----------
        data : array-like of shape (n_samples, n_features)
            The input data samples.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The predicted values.
        """
        model = self._load_model()
        data = self._scale_data(data)
        self.logger.info(f"Data shape after scaling: {data.shape}")
        return model.predict(data)

    def _scale_data(self, data: "ndarray") -> "ndarray":
        """
        scale the input data.

        Parameters
        ----------
        data : array-like of shape (n_samples, n_features)
            The input data samples.

        Returns
        -------
        X : ndarray of shape (n_samples, n_features)
            The scaled input data.
        """
        scaler = self._load_scaler()
        self.logger.info(f"Scaling data with {self.model_name}")
        return scaler.transform(data)
