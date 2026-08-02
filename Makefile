.PHONY: help build up down logs shell test lint format clean dev-build dev-up dev-down

help:
	@echo "Available commands:"
	@echo "  make build       - Build Docker images"
	@echo "  make up          - Start production containers"
	@echo "  make down        - Stop all containers"
	@echo "  make logs        - View container logs"
	@echo "  make shell       - Open shell in Airflow webserver container"
	@echo "  make test        - Run tests in development container"
	@echo "  make lint        - Run code linting in development container"
	@echo "  make format      - Format code in development container"
	@echo "  make clean       - Clean up volumes and containers"
	@echo "  make dev-build   - Build development image"
	@echo "  make dev-up      - Start development containers"
	@echo "  make dev-down    - Stop development containers"

build:
	docker-compose -f docker/docker-compose.yml build

up:
	docker-compose -f docker/docker-compose.yml up -d

down:
	docker-compose -f docker/docker-compose.yml down

logs:
	docker-compose -f docker/docker-compose.yml logs -f

shell:
	docker-compose -f docker/docker-compose.yml exec airflow-webserver bash

test:
	docker-compose -f docker/docker-compose.dev.yml exec app pytest tests/

lint:
	docker-compose -f docker/docker-compose.dev.yml exec app flake8 src/ tests/

format:
	docker-compose -f docker/docker-compose.dev.yml exec app black src/ tests/
	docker-compose -f docker/docker-compose.dev.yml exec app isort src/ tests/

clean:
	docker-compose -f docker/docker-compose.yml down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

dev-build:
	docker-compose -f docker/docker-compose.dev.yml build

dev-up:
	docker-compose -f docker/docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker/docker-compose.dev.yml down

airflow-init:
	docker-compose -f docker/docker-compose.yml exec airflow-webserver airflow db init

airflow-create-user:
	docker-compose -f docker/docker-compose.yml exec airflow-webserver airflow users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com

airflow-version:
	docker-compose -f docker/docker-compose.yml exec airflow-webserver airflow version

dbt-run:
	docker-compose -f docker/docker-compose.yml exec dbt dbt run

dbt-test:
	docker-compose -f docker/docker-compose.yml exec dbt dbt test

dbt-docs:
	docker-compose -f docker/docker-compose.yml exec dbt dbt docs generate
