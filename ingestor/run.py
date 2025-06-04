# This file is used to run the Flask application.git
from ingestor.config import load_config
from ingestor.src.app import create_app

config = load_config()
print(config.PREDICTOR_URL)

app = create_app(config=config)


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT, host="0.0.0.0")
