# Entry point for the application
# This file is used to run the Flask application.git
from predictor.config import load_config
from predictor.src.app import create_app

config = load_config()
print(config)
app = create_app(config=config)

if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT, host="0.0.0.0")
