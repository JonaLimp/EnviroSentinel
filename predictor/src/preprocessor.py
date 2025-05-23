from collections import deque
from typing import Any, Deque, Dict, List

import joblib
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder


class Preprocessor:
    def __init__(
        self,
        is_training: bool,
        sound_encoder_path: str = "",
        station_encoder_path: str = "",
        history_size: int = 10,
    ):
        self.history: Deque[Any] = deque(maxlen=history_size)
        self.columns = {
            "Temperatur": "value_Temperatur",
            "rel. Luftfeuchte": "value_Luftfeuchte",
            "Lautstärke": "value_Lautstärke",
        }

        self.expected_cols = [
            "value_Temperatur",
            "value_Luftfeuchte",
            "value_Lautstärke",
            "hour",
            "minute",
            "weekday",
            "is_weekend",
            "is_daylight",
            "value_Temperatur_rolling_mean",
            "value_Temperatur_rolling_std",
            "value_Temperatur_diff",
            "value_Luftfeuchte_rolling_mean",
            "value_Luftfeuchte_rolling_std",
            "value_Luftfeuchte_diff",
            "sound_high",
            "sound_silent",
            "sound_bin_encoded",
            "station_encoded",
        ]

        self.is_training = is_training

        if not is_training:
            self._sound_encoder = joblib.load(sound_encoder_path)
            self._station_encoder = joblib.load(station_encoder_path)
        else:
            self._sound_encoder = OrdinalEncoder()
            self._station_encoder = OrdinalEncoder()

    def fit_encoders(self, sound_bins: List[str], stations: List[str]):
        sound_df = pd.DataFrame(
            [[s] for s in sorted(set(sound_bins))], columns=["sound_bin"]
        )
        station_df = pd.DataFrame(
            [[s.replace(" ", "_")] for s in sorted(set(stations))], columns=["station"]
        )
        self._sound_encoder.fit(sound_df)
        self._station_encoder.fit(station_df)

    def save_encoders(self, sound_path: str, station_path: str):
        joblib.dump(self._sound_encoder, sound_path)
        joblib.dump(self._station_encoder, station_path)

    def decode_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["sound_bin"] = self._sound_encoder.inverse_transform(
            df[["sound_bin_encoded"]]
        )[:, 0]
        df["station"] = self._station_encoder.inverse_transform(
            df[["station_encoded"]]
        )[:, 0]
        return df

    def _add_features(
        self, full: pd.DataFrame, latest: pd.DataFrame, station: str
    ) -> pd.DataFrame:
        latest["hour"] = latest.index.hour
        latest["minute"] = latest.index.minute
        latest["weekday"] = latest.index.weekday
        latest["is_weekend"] = latest["weekday"].isin([5, 6]).astype(int)
        latest["is_daylight"] = ((latest["hour"] >= 6) & (latest["hour"] <= 20)).astype(
            int
        )

        for col in ["value_Temperatur", "value_Luftfeuchte"]:
            latest[f"{col}_rolling_mean"] = (
                full[col].rolling(5, min_periods=1).mean().iloc[-1]
            )
            latest[f"{col}_rolling_std"] = (
                full[col].rolling(5, min_periods=1).std().iloc[-1]
            )
            latest[f"{col}_diff"] = full[col].diff().iloc[-1]

        latest["sound_high"] = (latest["value_Lautstärke"] > 100).astype(int)
        latest["sound_silent"] = (latest["value_Lautstärke"] < 10).astype(int)

        latest["sound_bin"] = pd.cut(
            latest["value_Lautstärke"],
            bins=[0, 30, 60, 90, 120],
            labels=["very quiet", "quiet", "normal", "loud"],
        )

        latest["sound_bin_encoded"] = self._sound_encoder.transform(
            latest[["sound_bin"]]
        )
        latest["station_encoded"] = self._station_encoder.transform(
            [[station.replace(" ", "_")]]
        )

        latest.drop(columns=["sound_bin"], inplace=True)
        latest.fillna(0, inplace=True)
        return latest.reindex(columns=self.expected_cols, fill_value=0)

    def transform_from_sensor_data(
        self, sensor_data: Dict[str, Dict], box_name: str
    ) -> List[float]:
        ts = pd.to_datetime(sensor_data["Temperatur"]["timestamp"])
        row = {
            "timestamp": ts,
            **{self.columns[key]: sensor_data[key]["value"] for key in self.columns},
        }

        df = pd.DataFrame([row]).set_index("timestamp")
        self.history.append(df)

        full = pd.concat(list(self.history)).sort_index()
        latest = full.iloc[[-1]].copy()

        processed = self._add_features(full, latest, box_name)
        return processed.iloc[0].tolist()

    def transform_from_dataframe(
        self, df: pd.DataFrame, station_name: str
    ) -> pd.DataFrame:
        df = df.copy()
        df.index = pd.to_datetime(df.index)

        # Rename to expected columns
        df.rename(columns=self.columns, inplace=True)

        # Time-based
        df["hour"] = df.index.hour
        df["minute"] = df.index.minute
        df["weekday"] = df.index.weekday
        df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)
        df["is_daylight"] = ((df["hour"] >= 6) & (df["hour"] <= 20)).astype(int)

        # Rolling + diffs
        for col in ["value_Temperatur", "value_Luftfeuchte"]:
            df[f"{col}_rolling_mean"] = df[col].rolling(5, min_periods=1).mean()
            df[f"{col}_rolling_std"] = df[col].rolling(5, min_periods=1).std()
            df[f"{col}_diff"] = df[col].diff()

        # Sound flags
        df["sound_high"] = (df["value_Lautstärke"] > 100).astype(int)
        df["sound_silent"] = (df["value_Lautstärke"] < 10).astype(int)

        # Sound bin
        df["sound_bin"] = pd.cut(
            df["value_Lautstärke"],
            bins=[0, 30, 60, 90, 120],
            labels=["very quiet", "quiet", "normal", "loud"],
        )

        # Encode station + sound bin
        df["station"] = station_name.replace(" ", "_")
        df["sound_bin_encoded"] = self._sound_encoder.transform(df[["sound_bin"]])
        df["station_encoded"] = self._station_encoder.transform(df[["station"]])

        # Cleanup
        df.drop(columns=["sound_bin", "station"], inplace=True)
        df.fillna(0, inplace=True)

        # Reorder to expected columns
        df = df.reindex(columns=self.expected_cols, fill_value=0)
        print(df.columns)
        return df
