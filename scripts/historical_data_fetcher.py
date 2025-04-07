import json
from datetime import datetime, timedelta
from pathlib import Path

import requests

dir_path = Path("raw_data")
if not dir_path.exists():
    dir_path.mkdir()

with open("sensors.json") as f:
    sensor_config = json.load(f)

config_sensor_types = sensor_config["sensor_types"]
sensor_boxes = sensor_config["boxes"]

start_date = datetime.utcnow().date() - timedelta(days=1)
start_datetime = datetime.combine(start_date, datetime.min.time())
end_date = start_date - timedelta(days=30)
chunk_days = 1


for box_name, box_content in sensor_boxes.items():
    box_path = Path(dir_path) / box_name
    if not box_path.exists():
        box_path.mkdir()

    print(box_name)
    box_id = box_content["box_id"]
    url = f"https://api.opensensemap.org/boxes/{box_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching box info.")
        continue

    box_data = response.json()
    sensors = box_data.get("sensors", [])

    current_end = start_date

    for sensor in sensors:
        sensor_id = sensor["_id"]

        if sensor["title"] not in config_sensor_types:
            continue
        print(sensor["title"])
        while current_end > end_date:
            current_start = max(current_end - timedelta(days=chunk_days - 1), end_date)

            from_str = current_start.strftime("%Y-%m-%dT23:59:59Z")
            to_str = current_end.strftime("%Y-%m-%dT23:59:59Z")

            csv_url = (
                f"https://api.opensensemap.org/boxes/{box_id}/data/{sensor_id}"
                f"?from={from_str}&to={to_str}&format=csv"
            )

            csv_response = requests.get(csv_url)

            if response.status_code != 200:
                print("error!")

            csv_data = csv_response.text

            file_path = (
                box_path
                / f"{box_name.replace(' ', '_')}_{sensor['title']}_{current_start}.csv"
            )
            with file_path.open("w") as f:
                f.write(csv_data)
            current_end = current_start - timedelta(days=1)
