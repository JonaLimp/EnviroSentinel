# data_ingest/Dockerfile

FROM python:3.11-slim

# Set workdir inside the container
WORKDIR /app

# Copy and install dependencies
COPY data_ingest/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire package so imports like `from data_ingest...` work
COPY data_ingest/ ./data_ingest/
COPY sensor_config.json ./ 

# Set PYTHONPATH to make data_ingest importable
ENV PYTHONPATH=/app

# Run the microservice
CMD ["python", "data_ingest/run.py"]
