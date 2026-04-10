.PHONY: help build up down restart logs shell test lint typecheck format clean

COMPOSE = docker compose

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

# ── Docker ───────────────────────────────────────────────────────────

build: ## Build the Docker image
	$(COMPOSE) build

up: ## Start services in the background
	$(COMPOSE) up -d

down: ## Stop and remove services
	$(COMPOSE) down

restart: down up ## Restart all services

logs: ## Tail service logs
	$(COMPOSE) logs -f

shell: ## Open a shell inside the running container
	$(COMPOSE) exec admin-meta-agents /bin/bash || \
		$(COMPOSE) exec admin-meta-agents /bin/sh

# ── Development ──────────────────────────────────────────────────────

install: ## Install the package with dev dependencies
	pip install -e ".[dev]"

test: ## Run the test suite with coverage
	python -m pytest tests/ -v --tb=short --cov=admin_meta_agents --cov-report=term-missing

lint: ## Run linter (ruff)
	python -m ruff check admin_meta_agents/ tests/ main.py

typecheck: ## Run type checker (mypy)
	python -m mypy admin_meta_agents/

format: ## Auto-format code (ruff)
	python -m ruff check --fix admin_meta_agents/ tests/ main.py
	python -m ruff format admin_meta_agents/ tests/ main.py

clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
