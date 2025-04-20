import json
from pathlib import Path

import pandas as pd

config = json.load(open("sensor_config.json"))
RESAMPLE = config["preprocessing"]["resample"]
START_DATE = config["preprocessing"]["start_date"]

RESAMPLE = True
RESAMPLE_INTERVAL = config["preprocessing"]["resample_interval"]

raw_data_path = Path("data/raw_data")
output_path = Path("data/merged_data")

output_path.mkdir(parents=True, exist_ok=True)

for box_dir in raw_data_path.iterdir():
    print(box_dir.name)
    sensor_dfs = {}

    for sensor_dir in box_dir.iterdir():
        print(sensor_dir.name)
        for file in sensor_dir.iterdir():
            sensor_df = pd.read_csv(file, dtype={"value": "float32", "timestamp": str})
            sensor_df.rename(columns={"createdAt": "timestamp"}, inplace=True)
            sensor_df["timestamp"] = pd.to_datetime(
                sensor_df["timestamp"], errors="coerce"
            )
            sensor_df.dropna(subset=["timestamp"], inplace=True)

            sensor_type = file.stem.split("_")[-2]

            if RESAMPLE:
                sensor_df.set_index("timestamp", inplace=True)
                sensor_df = sensor_df.resample(RESAMPLE_INTERVAL).mean()
                sensor_df.reset_index(inplace=True)

            if sensor_type not in sensor_dfs:
                sensor_dfs[sensor_type] = sensor_df
            else:
                sensor_dfs[sensor_type] = pd.concat(
                    [sensor_dfs[sensor_type], sensor_df], axis=0
                )

    box_sensors_data = list(sensor_dfs.values())

    for idx, (sensor_type, sensor_df) in enumerate(sensor_dfs.items()):
        sensor_df.rename(columns={"value": f"value_{sensor_type}"}, inplace=True)
        sensor_df.sort_values("timestamp")
        sensor_df.drop_duplicates(subset=["timestamp"], keep="first", inplace=True)

        print(f"Merge {sensor_type} data")
        if idx == 0:
            merged_box_data = sensor_df
        else:
            merged_box_data = pd.merge(
                merged_box_data, sensor_df, on="timestamp", how="outer"
            )

    merged_box_data.sort_values("timestamp", inplace=True)

    print(f"Writing to {output_path / f'{box_dir.name}.csv'}")
    merged_box_data.to_csv(output_path / f"{box_dir.name}.csv", index=False)
