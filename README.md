
# Conceptual Architecture: IoT Anomaly Detection System

This document outlines the high-level architecture of the anomaly detection platform using microservices, real-time sensor data from OpenSenseMap, and a standalone model training pipeline.

---

## Data Source

### OpenSenseMap
[OpenSenseMap](https://opensensemap.org/) is a crowdsourced environmental sensing platform where individuals and organizations can publish data from their personal or deployed IoT sensors.

**Used Phenomena**

- Temperature (`temperature`)
- Humidity (`humidity`)
- Sound level / Noise (`sound level`)

**Access via API**

Example endpoint to fetch latest data for a specific box:

```
GET https://api.opensensemap.org/boxes/{boxId}/data
```

You can also filter by phenomenon:

```
GET https://api.opensensemap.org/boxes/{boxId}?phenomenon=temperature
```

---

## Microservices Overview

### `data_ingest` Microservice
Responsible for acquiring real-time data from OpenSenseMap and optionally forwarding it to the predictor.

**Key Components**

| File                  | Class              | Responsibility                              |
|-----------------------|--------------------|----------------------------------------------|
| `opensense_service.py`| `OpenSenseFetcher` | Fetch data from OpenSenseMap API             |
| `sender.py`           | `PredictorSender`  | POST data to the predictor microservice      |
| `routes.py`           | Flask Route        | Expose `/ingest` to trigger data acquisition |
| `config.py`           | `DataIngestConfig` | Holds env settings: API keys, box IDs, etc.  |

---

### `predictor` Microservice
Loads a trained ML model, accepts POSTs to `/predict`, and returns anomaly detection results.

**Key Components**

| File             | Class       | Responsibility                                |
|------------------|-------------|-----------------------------------------------|
| `model_service.py` | `Predictor` | Load ML model and perform predictions         |
| `routes.py`        | Flask Route| Expose `/predict` API                         |
| `config.py`        | Config     | Holds model path, thresholds, etc.            |

---

### `training` Module
This standalone module is responsible for preparing data, training the anomaly detection model, and exporting the model for use in production.

**Key Components**

| File                  | Class or Function      | Responsibility                               |
|-----------------------|------------------------|-----------------------------------------------|
| `train_model.py`      | `train()`              | Loads, preprocesses, and trains model         |
| `preprocessing.py`    | `clean_data()`         | Cleans and prepares raw data for training     |
| `model_exporter.py`   | `save_model()`         | Serializes and saves model to disk (`.pkl`)   |
| `config.py`           | `TrainingConfig`       | Data paths, output directory, hyperparameters |

---

### `data_fetching` Submodule (inside training)
Provides reusable tools to acquire and prepare training data from OpenSenseMap and other sources.

**Suggested Structure**

```
training/
├── data_fetching/
│   ├── __init__.py
│   ├── opensense_fetcher.py   # fetch_from_box(box_id, start, end)
│   ├── merger.py              # combine multiple boxes/sources
│   └── exporter.py            # save_to_csv(data, filename)
└── fetch_training_data.py     # entrypoint to build training dataset
```

---

## API Endpoints

| Microservice   | Method | Endpoint     | Description                                 |
|----------------|--------|--------------|---------------------------------------------|
| `data_ingest`  | GET    | `/ingest`    | Fetch from OpenSenseMap & forward to model  |
| `predictor`    | POST   | `/predict`   | Accepts features, returns anomaly result    |

---

## Config-Driven Design

Each microservice and the training module use their own `.env` file and `config.py`, with variables such as:

- `MODEL_PATH`
- `LOG_LEVEL`
- `PREDICTOR_URL`
- `OPENSENSEMAP_BOX_ID`
- `TRAIN_DATA_PATH`, `MODEL_OUTPUT_PATH`

All are loaded via a `load_config()` function pattern, with environment-specific `.env.development`, `.env.production`, etc.

---