# Makefile for project automation

.PHONY: install test lint format clean docker-build docker-run

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src tests
	
format:
	black src tests
	isort src tests

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name 'htmlcov' -exec rm -rf {} +
	find . -type f -name '.coverage' -delete

prepare-data:
	python -m src.data.load_data

train:
	python scripts/train_models.py

monitor-drift:
	python scripts/monitor_drift.py

run-api:
	uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t credit-default-api:latest .

docker-run:
	docker run -p 8000:8000 credit-default-api:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

dvc-repro:
	dvc repro

mlflow-ui:
	mlflow ui

all: install prepare-data train test
