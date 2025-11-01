# Makefile for HTW Emerging Photo

.PHONY: help setup install run-backend run-frontend run-docker test clean lint format

help:
	@echo "HTW Emerging Photo - Available Commands"
	@echo "========================================"
	@echo "setup          - Initial project setup"
	@echo "install        - Install dependencies"
	@echo "run-backend    - Run FastAPI backend"
	@echo "run-frontend   - Run Streamlit frontend"
	@echo "run-docker     - Run with Docker Compose"
	@echo "test           - Run tests"
	@echo "lint           - Run linters"
	@echo "format         - Format code"
	@echo "clean          - Clean temporary files"

setup:
	@echo "🚀 Setting up project..."
	./scripts/setup.sh

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

run-backend:
	@echo "🚀 Starting backend..."
	./scripts/run_backend.sh

run-frontend:
	@echo "🚀 Starting frontend..."
	./scripts/run_frontend.sh

run-docker:
	@echo "🐳 Starting with Docker..."
	docker-compose up --build

test:
	@echo "🧪 Running tests..."
	./scripts/run_tests.sh

lint:
	@echo "🔍 Running linters..."
	flake8 src/ tests/
	mypy src/

format:
	@echo "✨ Formatting code..."
	black src/ tests/ frontend/

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build/ dist/
	@echo "✅ Clean complete!"

