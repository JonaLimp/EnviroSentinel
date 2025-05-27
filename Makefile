-include ingestor/.env.development
ingestor_PORT := $(PORT)

-include predictor/.env.development
predictor_PORT := $(PORT)


# Export Poetry dependencies to requirements.txt (if needed)
requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

# Build Docker images
build-data-ingest:
	docker build -f ingestor/Dockerfile -t ingestor .

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
	-@docker rm -f ingestor_service 2>/dev/null || true
	docker build -f ingestor/Dockerfile -t ingestor .
	docker run --rm --name ingestor_service \
	  --env-file ingestor/.env.development \
	  -e PYTHONPATH=/app \
	  -p 5002:$(ingestor_PORT) \
	  ingestor

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
	docker exec -it ingestor_service /bin/sh

shell-predictor:
	docker exec -it predictor_service /bin/sh
