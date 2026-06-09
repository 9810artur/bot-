"""Makefile for LocalAdsBot."""

.PHONY: help install test lint format run docker-up docker-down migrate

help:                         ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:                      ## Install dependencies
	pip install -r requirements.txt

test:                         ## Run tests
	pytest

test-cov:                     ## Run tests with coverage
	pytest --cov=src --cov-report=html

lint:                         ## Run linters
	black src/ tests/
	flake8 src/ tests/
	mypy src/

format:                       ## Format code with Black
	black src/ tests/

run:                          ## Run bot locally
	python -m src.main

docker-build:                 ## Build Docker image
	docker-compose build

docker-up:                    ## Start Docker containers
	docker-compose up -d

docker-down:                  ## Stop Docker containers
	docker-compose down

docker-logs:                  ## Show Docker logs
	docker-compose logs -f app

migrate:                      ## Apply database migrations
	alembic upgrade head

migrate-create:               ## Create new migration
	alembic revision --autogenerate -m "$(MESSAGE)"

migrate-downgrade:            ## Downgrade one migration
	alembic downgrade -1

env:                          ## Create .env file from example
	cp .env.example .env

clean:                        ## Clean up cache files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

db-reset:                     ## Reset database (Docker)
	docker-compose down -v
	docker-compose up -d postgres

docs:                         ## Generate documentation
	@echo "Documentation is in README.md"

.DEFAULT_GOAL := help
