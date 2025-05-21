# Use a minimal Python image
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install dependencies
COPY predictor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the predictor codebase
COPY predictor/ ./predictor/
COPY model/ ./model/ 

# Set PYTHONPATH so imports like `from predictor.config` work
ENV PYTHONPATH=/app

# Start the microservice (adjust if using Flask, FastAPI, etc.)
CMD ["python", "predictor/run.py"]

