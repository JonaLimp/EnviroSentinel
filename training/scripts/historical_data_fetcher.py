import json
from datetime import datetime, timedelta
from pathlib import Path

import requests

config = json.load(open("sensor_config.json"))
FETCH_INTERVAL = config["preprocessing"]["fetch_interval"]
START_DATE = config["preprocessing"]["start_date"]

with open("sensor_config.json") as f:
    sensor_config = json.load(f)

config_sensor_types = sensor_config["sensor_types"]
sensor_boxes = sensor_config["boxes"]

if START_DATE == "now":
    start_date = datetime.utcnow().date()
else:
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d").date()

start_date = start_date - timedelta(days=1)
start_datetime = datetime.combine(start_date, datetime.min.time())
end_date = start_date - timedelta(days=FETCH_INTERVAL)
chunk_days = 1

for box_name, box_content in sensor_boxes.items():
    print(f"Processing box: {box_name}")
    box_id = box_content["box_id"]
    url = f"https://api.opensensemap.org/boxes/{box_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching box info.")
        continue

    box_data = response.json()
    sensors = box_data.get("sensors", [])

    for sensor in sensors:
        current_end = start_date
        sensor_id = sensor["_id"]

        if sensor["title"] not in config_sensor_types:
            continue

        print(f"Processing sensor: {sensor['title']}")

        while current_end > end_date:
            current_start = max(current_end - timedelta(days=chunk_days - 1), end_date)
            from_str = current_start.strftime("%Y-%m-%dT00:00:00Z")
            to_str = current_end.strftime("%Y-%m-%dT23:59:59Z")

            csv_url = (
                f"https://api.opensensemap.org/boxes/{box_id}/data/{sensor_id}"
                f"?from-date={from_str}&to-date={to_str}&format=csv"
            )

            csv_response = requests.get(csv_url)

            if csv_response.status_code != 200:
                print(
                    f"Error fetching data for {sensor['title']}"
                    f" from {from_str} to {to_str}"
                )
                continue

            csv_data = csv_response.text

            if not csv_data.strip():
                print(f"No data for {sensor['title']} between {from_str} and {to_str}.")
                continue

            file_path = (
                Path("data/raw_data")
                / box_name.replace(" ", "_")
                / Path(sensor["title"].replace(" ", "_"))
                / f"{box_name.replace(' ', '_')}_"
                f"{sensor['title'].replace(' ', '_')}_{current_start}.csv"
            )

            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)

            print(
                f"Writing data for {sensor['title']}"
                f" between {from_str} and {to_str} to {file_path}"
            )
            with file_path.open("w", encoding="utf-8") as f:
                f.write(csv_data)

            current_end = current_start - timedelta(days=1)
