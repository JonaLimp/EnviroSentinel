# config.py
import os
from pathlib import Path

# Root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default model directory and paths
MODEL_DIR = PROJECT_ROOT / "model"

# Flask environment settings
FLASK_ENV = os.getenv("FLASK_ENV", "development")
PORT = int(os.getenv("PORT", 5000))
