from flask import current_app, jsonify

from ingestor.src.blueprint import ingestor_bp
from ingestor.src.opensense_service import OpenSenseFetcher
from ingestor.src.sender import PredictorSender


@ingestor_bp.route("/ingest", methods=["GET"])
def ingest():
    config = current_app.config["CONFIG"]
    box_ids = config.BOX_IDS
    sender = PredictorSender(config.PREDICTOR_URL)
    results = []

    fetcher = OpenSenseFetcher(config.BASE_URL, config.SENSOR_TYPES)

    for box_name, box_id in box_ids.items():
        try:
            data = fetcher.fetch_latest(box_id=box_id)
            current_app.logger.debug(f"Fetched data for {box_name}: {data}")

            box_data = {
                "box_name": box_name,
                "box_id": box_id,
                "data": data,
            }
            print(f"Box data: {box_data}")
            prediction = sender.send(box_data)

            results.append({**box_data, "prediction": prediction})

        except Exception as e:
            results.append({"box_id": box_id, "error": str(e)})

    return jsonify(results)
