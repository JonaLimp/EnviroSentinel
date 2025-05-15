# This file is used to run the Flask application.git
from data_ingest.config import load_data_ingest_config
from predictor.src.app import create_app

app = create_app(load_data_ingest_config())

if __name__ == "__main__":
    app.run()
