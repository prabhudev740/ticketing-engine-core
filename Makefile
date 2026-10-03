.PHONY: help up down build logs gateway-dev migrate test clean

# Default target when running just 'make'
help:
	@echo "=================================================="
	@echo " Ticketing Engine Core - Monorepo Makefile"
	@echo "=================================================="
	@echo "  make up              - Start infrastructure (Postgres, Redis, Consul) via Docker"
	@echo "  make down            - Stop infrastructure containers"
	@echo "  make build           - Rebuild all Docker service containers"
	@echo "  make logs            - Tail container logs across services"
	@echo "  make run             - Run the API Gateway locally with uv & uvicorn"
	@echo "  make migrate         - Run Alembic database migrations for the Gateway"
	@echo "  make test            - Run the Pytest test suite"
	@echo "  make clean           - Remove python cache and build artifacts"
	@echo "=================================================="

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

run:
	cd services/gateway && uv run uvicorn app.main:app --reload --port 8000

migrate:
	cd services/gateway && uv run alembic upgrade head

test:
	pytest tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +