-include data_ingest/.env.development
data_ingest_PORT := $(PORT)

-include predictor/.env.development
predictor_PORT := $(PORT)


# Export Poetry dependencies to requirements.txt (if needed)
requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

# Build Docker images
build-data-ingest:
	docker build -f data_ingest/Dockerfile -t data_ingest .

build-predictor:
	docker build -f predictor/Dockerfile -t predictor .

# Run containers with env + dynamic port binding
run-predictor:
	-@docker rm -f predictor_service 2>/dev/null || true
	docker build -f predictor/Dockerfile -t predictor .
	docker run --rm --name predictor_service \
	  --env-file predictor/.env.development \
	  -e PYTHONPATH=/app \
	  -p 5001:$(predictor_PORT) \
	  predictor

run-data-ingest:
	-@docker rm -f data_ingest_service 2>/dev/null || true
	docker build -f data_ingest/Dockerfile -t data_ingest .
	docker run --rm --name data_ingest_service \
	  --env-file data_ingest/.env.development \
	  -e PYTHONPATH=/app \
	  -p 5002:$(data_ingest_PORT) \
	  data_ingest

.PHONY: build up down restart logs shell

# Default Compose file
COMPOSE_FILE=docker-compose.yml

build:
	docker-compose -f $(COMPOSE_FILE) build

up:
	docker-compose -f $(COMPOSE_FILE) up --build

down:
	docker-compose -f $(COMPOSE_FILE) down

restart:
	docker-compose -f $(COMPOSE_FILE) down
	docker-compose -f $(COMPOSE_FILE) up --build

logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

shell-data-ingest:
	docker exec -it data_ingest_service /bin/sh

shell-predictor:
	docker exec -it predictor_service /bin/sh
