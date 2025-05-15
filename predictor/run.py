# Entry point for the application
# This file is used to run the Flask application.git
from predictor.config import load_predictor_config
from predictor.src.app import create_app

app = create_app(load_predictor_config())

if __name__ == "__main__":
    app.run(debug=True)
