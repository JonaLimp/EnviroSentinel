from flask import current_app, jsonify

from data_ingest.src.blueprint import ingestor_bp
from data_ingest.src.opensense_service import OpenSenseFetcher
from data_ingest.src.sender import PredictorSender


@ingestor_bp.route("/ingest", methods=["GET"])
def ingest():
    config = current_app.config["CONFIG"]
    box_ids = config.BOX_IDS
    sender = PredictorSender(config.PREDICTOR_URL)
    results = []

    for name, box_id in box_ids.items():
        try:
            fetcher = OpenSenseFetcher(config.BASE_URL, config.SENSOR_TYPES)
            data = fetcher.fetch_latest(box_id=box_id)
            prediction = sender.send(data)
            results.append(
                {
                    "box_name": name,
                    "box_id": box_id,
                    "input": data,
                    "prediction": prediction,
                }
            )
        except Exception as e:
            results.append({"box_id": box_id, "error": str(e)})

    return jsonify(results)
