.PHONY: help install test lint format docker-build docker-up docker-down tf-init tf-plan tf-apply helm-lint deploy-dev clean

PYTHON ?= python3
ENV ?= dev

help:
	@echo "National GDP Prediction Service - Developer CLI"
	@echo "--------------------------------------------------"
	@echo "make install       - Install Python dependencies"
	@echo "make test          - Run unit & integration tests with coverage"
	@echo "make lint          - Run flake8 and black formatting checks"
	@echo "make format        - Auto-format code with black"
	@echo "make docker-build  - Build multi-stage Docker image"
	@echo "make docker-up     - Start local stack (App, Postgres, Redis, Prometheus, Grafana)"
	@echo "make docker-down   - Stop local stack"
	@echo "make tf-init       - Initialize Terraform"
	@echo "make tf-plan       - Plan Terraform changes for ENV=$(ENV)"
	@echo "make tf-apply      - Apply Terraform infrastructure for ENV=$(ENV)"
	@echo "make helm-lint     - Lint Helm Chart"
	@echo "make deploy-dev    - Deploy to Dev EKS cluster"
	@echo "make clean         - Clean bytecode & temporary test files"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r src/requirements.txt

test:
	pytest --cov=src --cov-report=term-missing tests/

lint:
	flake8 src tests --max-line-length=120 --ignore=E203,W503
	black --check src tests

format:
	black src tests

docker-build:
	docker build -t gdp-prediction-app:latest .

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down -v

tf-init:
	cd terraform && terraform init

tf-plan:
	cd terraform/environments/$(ENV) && terraform init && terraform plan

tf-apply:
	cd terraform/environments/$(ENV) && terraform init && terraform apply -auto-approve

helm-lint:
	helm lint helm/gdp-prediction-app/

deploy-dev:
	helm upgrade --install gdp-app-dev ./helm/gdp-prediction-app \
		--namespace gdp-dev --create-namespace \
		--values ./helm/gdp-prediction-app/values-dev.yaml

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage coverage.xml
