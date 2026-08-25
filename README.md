# 📈 National GDP Prediction Platform — Production Infrastructure & CI/CD Platform

Production-grade cloud platform, containerization, Infrastructure as Code (Terraform), Kubernetes (AWS EKS), GitOps (Argo CD), and DevSecOps CI/CD pipeline for the **National GDP Prediction Engine** (ARIMA + Deep Learning Hybrid Models).

---

## 🏛️ Architecture Overview

```mermaid
graph TD
    Dev[Developer] -->|Git Commit| GH[GitHub Repo]
    GH -->|PR Trigger| CI[GitHub Actions CI Pipeline]
    
    subgraph Security & Quality Gates
        CI -->|Lint & Test| PYTEST[Flake8 / Pytest]
        CI -->|Security Scan| SEC[Bandit / Gitleaks / Trivy / TFSec]
        CI -->|Build Image| DOCKER[Docker Multi-Stage]
    end
    
    DOCKER -->|Push Image| ECR[AWS ECR Private Registry]

    subgraph AWS Cloud Platform (Terraform Managed)
        subgraph VPC Network (10.30.0.0/16)
            ALB[AWS Application Load Balancer]
            
            subgraph Private Subnets
                EKS[AWS EKS Cluster v1.30]
                ING[ALB Ingress Controller]
                PODS[FastAPI GDP Prediction Pods]
            end
            
            subgraph Isolated Database Subnets
                RDS[(AWS RDS PostgreSQL Multi-AZ)]
                REDIS[(AWS ElastiCache Redis)]
            end
        end

        S3[(AWS S3 Model Artifact Storage)]
    end

    ARGO[Argo CD GitOps] -->|Sync Helm Manifests| EKS
    ALB --> ING --> PODS
    PODS --> RDS & REDIS & S3
```

---

## 📂 Repository Structure

```
.
├── src/                                 # Production FastAPI Python ML Application
│   ├── app/
│   │   ├── api/                         # /health, /ready, /metrics, /predict, /forecast
│   │   ├── core/                        # Settings & JSON Logging
│   │   ├── db/                          # Async PostgreSQL & Redis Clients
│   │   ├── models/                      # ARIMA-LSTM/GRU/CNN Hybrid Machine Learning Engine
│   │   └── main.py                      # Application Entrypoint
│   └── data/GDP.csv                     # Historical GDP Dataset
├── tests/                               # Pytest Unit & Integration Suite
├── Dockerfile                           # Multi-stage Security-hardened Dockerfile
├── docker-compose.yml                   # Local Development Environment
├── terraform/                           # Modular Infrastructure as Code
│   ├── modules/                         # network, iam, ecr, eks, rds, redis, s3, monitoring
│   └── environments/                    # dev, staging, production
├── helm/                                # Production Kubernetes Helm Chart
│   └── gdp-prediction-app/
├── gitops/                              # Argo CD Manifests (App-of-Apps Pattern)
├── .github/workflows/                   # CI, CD-Dev, CD-Staging, CD-Production Pipelines
├── monitoring/                          # Prometheus Alerts & Grafana Dashboard
├── scripts/                             # Smoke test & DR Automation Scripts
├── docs/                                # Architecture, DR, Secrets & Troubleshooting Runbooks
└── Makefile                             # Developer CLI Command Automation
```

---

## ⚡ Quick Start & Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Terraform >= 1.7.0
- Helm 3

### 1. Run Local Environment
Spin up the FastAPI service, PostgreSQL, Redis, Prometheus, and Grafana in one command:
```bash
make docker-up
```
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
- **Prometheus Metrics**: [http://localhost:8000/metrics](http://localhost:8000/metrics)
- **Grafana Dashboard**: [http://localhost:3000](http://localhost:3000) (admin / admin)

### 2. Run Tests & Code Quality Checks
```bash
make test
make lint
```

---

## 🚀 Cloud Infrastructure & Deployment

### 1. Provision Infrastructure via Terraform
```bash
make tf-init
make tf-plan ENV=production
make tf-apply ENV=production
```

### 2. Deploy via Helm
```bash
make helm-lint
make deploy-dev
```

---

## 🛡️ Security & DevSecOps Controls
- **Non-Root Containers**: Runs as UID `10001` (`appuser`) with read-only root filesystem.
- **Automated Security Gates**: Gitleaks secret detection, Bandit SAST, Trivy container scanning, TFSec Terraform scanning.
- **Least Privilege IAM**: IRSA (IAM Roles for Service Accounts) used for AWS resource access.
