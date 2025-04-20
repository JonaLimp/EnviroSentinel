# Entry point for the application
# This file is used to run the Flask application.git
from src.app import create_app
from src.shared.config import load_config

config = load_config()
app = create_app(config)

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
