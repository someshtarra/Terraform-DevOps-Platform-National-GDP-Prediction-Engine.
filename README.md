# 🚀 Production DevOps & Infrastructure Platform: National GDP Prediction Engine

[![Terraform](https://img.shields.io/badge/Terraform-1.7%2B-623CE4?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS EKS](https://img.shields.io/badge/AWS_EKS-v1.30-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/eks/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)

An enterprise-grade, end-to-end cloud platform and CI/CD automation stack built with **AWS**, **Terraform**, **Kubernetes (EKS)**, **Docker**, **Helm**, **Argo CD**, **GitHub Actions**, and **Prometheus/Grafana**. 

This platform serves as a production environment for the **National GDP Prediction Engine**, a machine learning microservice that blends statistical time-series models (**ARIMA**) with sequence deep learning models (**LSTM / GRU / CNN**) to forecast national economic output with confidence intervals.

---

## 📑 Table of Contents

1. [Architectural Overview](#-1-architectural-overview)
2. [How the Platform Works](#-2-how-the-platform-works)
3. [Repository Directory Structure](#-3-repository-directory-structure)
4. [Prerequisites & System Requirements](#-4-prerequisites--system-requirements)
5. [Step-by-Step Installation & Setup Guide](#-5-step-by-step-installation--setup-guide)
   - [Step 5.1: Clone & Local Verification](#step-51-clone--local-verification)
   - [Step 5.2: Configure Credentials & Environment](#step-52-configure-credentials--environment)
   - [Step 5.3: Bootstrap Remote Terraform State](#step-53-bootstrap-remote-terraform-state)
   - [Step 5.4: Provision AWS Cloud & Kubernetes Infrastructure](#step-54-provision-aws-cloud--kubernetes-infrastructure)
   - [Step 5.5: Configure GitHub OIDC & Repository Settings](#step-55-configure-github-oidc--repository-settings)
6. [Local Development & Docker Execution](#-6-local-development--docker-execution)
7. [CI/CD Pipeline Workflow Explained](#-7-cicd-pipeline-workflow-explained)
8. [Kubernetes Workloads & Auto-scaling](#-8-kubernetes-workloads--auto-scaling)
9. [Observability, Metrics & Alerting](#-9-observability-metrics--alerting)
10. [Disaster Recovery & Rollback Procedures](#-10-disaster-recovery--rollback-procedures)
11. [Troubleshooting Guide](#-11-troubleshooting-guide)

---

## 🏛️ 1. Architectural Overview

The diagram below illustrates the end-to-end data flow and component topology from developer commit to multi-environment Kubernetes deployment:

```mermaid
graph TD
    subgraph Developer & Version Control
        DEV[Developer] -->|git push| GH[GitHub Repository]
    end

    subgraph CI/CD Pipeline - GitHub Actions
        GH -->|Push Trigger| CI_GATE[CI Quality & Security Gates]
        CI_GATE -->|1. Flake8 / Black| LINT[Lint & Code Style]
        CI_GATE -->|2. Pytest + Coverage| TEST[Unit & Integration Tests]
        CI_GATE -->|3. Bandit SAST & Gitleaks| SEC[Security & Secret Scan]
        CI_GATE -->|4. Docker Build & Trivy| SCAN[Container Vulnerability Scan]
        SCAN -->|5. Push Image| ECR[AWS ECR Private Registry]
    end

    subgraph AWS Cloud Infrastructure - Terraform Managed
        subgraph VPC Network - 10.30.0.0/16
            ALB[AWS Application Load Balancer]

            subgraph Public Subnets - AZ1 / AZ2 / AZ3
                IGW[Internet Gateway]
                NAT[NAT Gateways]
            end

            subgraph Private Subnets - EKS Nodes
                EKS[AWS EKS Cluster v1.30]
                ING[AWS Load Balancer Controller]
                POD1[FastAPI GDP Pod 1]
                POD2[FastAPI GDP Pod 2]
                HPA[Horizontal Pod Autoscaler]
            end

            subgraph Isolated Database Subnets
                RDS[(AWS RDS PostgreSQL Multi-AZ)]
                REDIS[(AWS ElastiCache Redis)]
            end
        end

        S3[(AWS S3 Model Artifact Storage)]
        SECMGR[AWS Secrets Manager]
        R53[Route 53 DNS]
        ACM[ACM TLS Certificate]
        CW[CloudWatch Logs]
    end

    subgraph Operations & GitOps
        ARGO[Argo CD] -->|Sync Helm Charts| EKS
        PROM[Prometheus & Grafana] -->|Scrape Metrics| POD1
    end

    ALB --> ING
    ING --> POD1 & POD2
    POD1 & POD2 --> RDS
    POD1 & POD2 --> REDIS
    POD1 & POD2 --> S3
```

---

## ⚙️ 2. How the Platform Works

1. **Machine Learning Service (`src/`)**: 
   - A FastAPI Python web application serving historical quarterly GDP observations and generating future 8-quarter projections.
   - Combines statistical linear trends (**ARIMA**) with deep learning residual networks (**LSTM / GRU / CNN**).
   - Serves endpoints: `/health` (Liveness), `/ready` (Readiness), `/metrics` (Prometheus exporter), `/api/v1/latest` (Data observation), `/api/v1/forecast` (Predictions with upper/lower bounds), and `/api/v1/models` (Model performance specs).
2. **Infrastructure as Code (`terraform/` & `aws/`)**: 
   - Terraform manages all AWS cloud resources declaratively.
   - Configures a 3-Tier Multi-AZ VPC network (Public, Private, Database subnets), EKS v1.30 Kubernetes cluster, ECR container registry, RDS PostgreSQL database, ElastiCache Redis cache, AWS Secrets Manager, Route 53 DNS, and ACM TLS Certificates.
3. **Containerization & Deployment (`Dockerfile`, `helm/`, `kubernetes/`)**:
   - Packaged into multi-stage, security-hardened Docker images running as non-root UID `10001` with read-only root filesystems.
   - Deployed onto EKS via Helm charts with Horizontal Pod Autoscaler (scaling from 2 to 15 pods), Pod Disruption Budgets, and Network Policy isolation.
4. **CI/CD & OIDC (`.github/workflows/` & `github/`)**:
   - Automated GitHub Actions pipelines for continuous integration and multi-environment deployment (`dev`, `staging`, `production`).
   - Uses AWS OpenID Connect (OIDC) federated authentication—eliminating the need to store long-lived AWS IAM access keys in GitHub.

---

## 📂 3. Repository Directory Structure

```text
TERRAFORM/
├── bootstrap/                           # Safe 2-Step Terraform State Bootstrap (S3 Bucket + DynamoDB)
│   ├── main.tf                          # S3 Bucket, DynamoDB Table, KMS Encryption Key
│   ├── variables.tf
│   └── outputs.tf
│
├── aws/                                 # AWS Cloud Infrastructure Resources
│   ├── vpc.tf                           # 3-AZ VPC, Public/Private/DB Subnets, NAT, IGW
│   ├── eks.tf                           # EKS Cluster v1.30, Node Groups & OIDC Provider
│   ├── ecr.tf                           # Immutable ECR Registry with scan-on-push
│   ├── rds.tf                           # PostgreSQL Multi-AZ DB Cluster in private subnets
│   ├── redis.tf                         # ElastiCache Redis Replication Group
│   ├── iam.tf                           # EKS Cluster & Worker Node IAM Roles
│   ├── secrets.tf                       # AWS Secrets Manager Secret & Versions
│   ├── dns.tf                           # Route 53 Hosted Zone
│   ├── acm.tf                           # ACM TLS Certificate with DNS Validation
│   └── monitoring.tf                    # CloudWatch Log Groups for EKS & Application
│
├── kubernetes/                          # Declarative Kubernetes Workloads
│   ├── namespace.tf                     # Application Namespace
│   ├── serviceaccount.tf                # EKS IRSA ServiceAccount
│   ├── rbac.tf                          # Role & RoleBinding
│   ├── configmap.tf                     # Environment ConfigMap
│   ├── deployment.tf                    # Rolling Update Deployment & SecurityContext
│   ├── service.tf                       # ClusterIP Service
│   ├── ingress.tf                       # AWS Load Balancer Controller Ingress
│   ├── hpa.tf                           # Horizontal Pod Autoscaler (2-15 pods)
│   ├── pdb.tf                           # Pod Disruption Budget
│   └── networkpolicy.tf                 # Network Policy Isolation
│
├── github/                              # GitHub Platform & OIDC Integration
│   ├── repository.tf                    # Repository settings management
│   ├── environments.tf                  # Dev, Staging, Production environments
│   ├── branch_protection.tf             # Main branch protection rules
│   ├── secrets.tf                       # Environment Secrets
│   └── oidc.tf                          # AWS IAM OIDC Provider & Roles
│
├── ci-cd/                               # GitHub Actions Workflow Templates
│   ├── ci.yml                           # Lint, Pytest, SAST & Docker Scan
│   ├── deploy-dev.yml                   # DEV Deployment
│   ├── deploy-staging.yml               # STAGING Deployment
│   └── deploy-production.yml            # PRODUCTION Deployment with Approval Gate
│
├── .github/workflows/                   # Live Active GitHub Actions Workflows
│   ├── pipeline.yml                     # Master End-to-End CI/CD Pipeline
│   ├── ci.yml                           # CI Quality Pipeline
│   ├── cd-dev.yml                       # Dev CD Pipeline
│   ├── cd-staging.yml                   # Staging CD Pipeline
│   └── cd-production.yml                # Production CD Pipeline
│
├── src/                                 # Production FastAPI Machine Learning Microservice
│   ├── app/
│   │   ├── api/                         # /health, /ready, /metrics, /predict, /forecast
│   │   ├── core/                        # Settings & Structured JSON Logging
│   │   ├── db/                          # Async PostgreSQL & Redis Clients
│   │   ├── models/                      # ARIMA-LSTM/GRU/CNN Hybrid ML Engine
│   │   └── main.py                      # FastAPI Server Entrypoint
│   └── data/GDP.csv                     # Historical GDP Dataset (1947-2024)
│
├── tests/                               # Pytest Unit & Integration Suite
├── Dockerfile                           # Security-Hardened Multi-Stage Dockerfile
├── docker-compose.yml                   # Local Development Stack
├── helm/                                # Production Kubernetes Helm Chart
│   └── gdp-prediction-app/
├── gitops/                              # Argo CD App-of-Apps Manifests
├── monitoring/                          # Prometheus Alert Rules & Grafana Dashboard
├── scripts/                             # Smoke Test, Health Check & DR Scripts
├── docs/                                # Architecture, DR, Secrets & Troubleshooting Runbooks
├── Makefile                             # Developer CLI Command Automation
├── terraform.tfvars.example             # Example Variables Template
└── README.md                            # Master Operating Documentation
```

---

## 🛠️ 4. Prerequisites & System Requirements

Before setting up the project, ensure you have the following installed on your local machine:

1. **Git**: `>= 2.30` ([Download](https://git-scm.com/))
2. **Docker & Docker Compose**: `>= 24.0` ([Download](https://www.docker.com/))
3. **Python**: `>= 3.11` ([Download](https://www.python.org/))
4. **Terraform**: `>= 1.7.0` ([Download](https://www.terraform.io/))
5. **AWS CLI**: `>= 2.15` ([Download](https://aws.amazon.com/cli/))
6. **Kubectl**: `>= 1.30` ([Download](https://kubernetes.io/docs/tasks/tools/))
7. **Helm**: `>= 3.14` ([Download](https://helm.sh/))

---

## 🚀 5. Step-by-Step Installation & Setup Guide

### Step 5.1: Clone & Local Verification

Clone the repository to your local environment:
```bash
git clone https://github.com/someshtarra/TERRAFORM.git
cd TERRAFORM
```

---

### Step 5.2: Configure Credentials & Environment

1. **Configure AWS CLI Credentials**:
   ```bash
   aws configure
   ```
   Provide your AWS Access Key ID, Secret Access Key, Default Region (`us-east-1`), and default output format (`json`).

2. **Prepare Terraform Variables**:
   Create your `terraform.tfvars` file from the provided template:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
   Edit `terraform.tfvars` and set your custom values:
   ```hcl
   aws_region        = "us-east-1"
   environment       = "production"
   project_name      = "gdp-prediction"
   vpc_cidr          = "10.30.0.0/16"
   cluster_name      = "gdp-eks"
   kubernetes_version = "1.30"
   db_instance_class = "db.m6g.large"
   db_name           = "gdp_db_prod"
   redis_node_type   = "cache.m6g.large"
   domain_name       = "gdp.api.domain.com"
   github_owner      = "someshtarra"
   github_repository = "TERRAFORM"
   github_token      = "ghp_YourPersonalAccessTokenGoesHere"
   ```

---

### Step 5.3: Bootstrap Remote Terraform State

Terraform requires an S3 bucket and DynamoDB table for remote state storage and state locking.

Run the automated bootstrap command:
```bash
make bootstrap
```

This command executes `terraform init` and `terraform apply` inside the `bootstrap/` directory, provisioning:
- **S3 Bucket**: `gdp-prediction-tf-state-bucket` (with KMS encryption & versioning enabled).
- **DynamoDB Table**: `gdp-prediction-tf-locks` (for state locking during concurrent applies).
- **KMS Key**: Dedicated customer-managed encryption key.

---

### Step 5.4: Provision AWS Cloud & Kubernetes Infrastructure

Initialize and apply the main Terraform workspace:

```bash
# 1. Initialize Terraform with the S3 remote backend
make init

# 2. Validate Terraform code syntax and dependencies
make validate

# 3. Preview all planned cloud resources (VPC, EKS, RDS, ECR, Redis, K8s)
make plan

# 4. Provision complete infrastructure to AWS
make apply
```

*(Type `yes` when prompted by Terraform to approve resource creation)*

---

### Step 5.5: Configure GitHub OIDC & Repository Settings

To allow GitHub Actions to deploy to AWS EKS securely without static AWS keys:

1. **Verify AWS IAM OIDC Role**:
   Terraform automatically provisions the IAM OIDC Role:
   `arn:aws:iam::<YOUR_ACCOUNT_ID>:role/gdp-github-actions-oidc-role-production`

2. **Add GitHub Repository Secrets**:
   Go to your GitHub Repository: **Settings → Secrets and variables → Actions → New repository secret** and add:
   - `AWS_ACCESS_KEY_ID`: *(Optional fallback access key if not using OIDC)*
   - `AWS_SECRET_ACCESS_KEY`: *(Optional fallback secret key)*

3. **Configure Environment Approval Gate**:
   - Navigate to **Settings → Environments → production**.
   - Enable **Required reviewers** and add your GitHub username. This ensures production deployments pause until you manually approve them in GitHub!

---

## 💻 6. Local Development & Docker Execution

You can run the entire platform locally on your laptop using Docker Compose without deploying to AWS:

### 1. Spin Up Local Stack
```bash
make docker-up
```
This launches 5 concurrent containers:
- **FastAPI Service**: `http://localhost:8000`
- **PostgreSQL Database**: `localhost:5432`
- **Redis Cache**: `localhost:6379`
- **Prometheus Server**: `http://localhost:9090`
- **Grafana Dashboard**: `http://localhost:3000` (Login: `admin` / `admin`)

### 2. Verify Local API Endpoints
- **Interactive Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint**: [http://localhost:8000/health](http://localhost:8000/health)
- **Readiness Check Endpoint**: [http://localhost:8000/ready](http://localhost:8000/ready)
- **Prometheus Metrics**: [http://localhost:8000/metrics](http://localhost:8000/metrics)
- **Get Latest GDP Observation**: [http://localhost:8000/api/v1/latest](http://localhost:8000/api/v1/latest)
- **Generate 8-Quarter Forecast**: 
  ```bash
  curl "http://localhost:8000/api/v1/forecast?quarters=8&model_type=ARIMA-LSTM"
  ```

### 3. Run Unit Tests & Linters
```bash
# Execute Pytest unit and integration test suite
make test

# Run code style & formatting checks
make lint
```

### 4. Stop Local Stack
```bash
make docker-down
```

---

## 🔄 7. CI/CD Pipeline Workflow Explained

The pipeline (`.github/workflows/pipeline.yml`) executes automatically whenever code is pushed to the `main` branch:

```text
git push
   │
   ▼
[1. CI Job: Lint, Test, Security & Docker Scan]
   ├── Black & Flake8 Code Linting
   ├── Pytest Unit & Integration Tests (Coverage Report)
   ├── Bandit SAST Static Code Analysis
   ├── Helm Chart Linting
   ├── Multi-Stage Docker Image Build
   └── Trivy Container Vulnerability Scan
   │
   ▼
[2. DEV Deployment Job]
   ├── Push Image to AWS ECR with <git-sha> Tag
   ├── Deploy Helm Chart to EKS 'gdp-dev' Namespace
   └── Execute Post-Deployment Smoke Tests (scripts/smoke_test.sh)
   │
   ▼
[3. STAGING Deployment Job]
   ├── Push Image to AWS ECR Staging Registry
   ├── Deploy Helm Chart to EKS 'gdp-staging' Namespace
   └── Execute Staging Integration Tests
   │
   ▼
[4. Manual Approval Gate (GitHub Environment)]
   └── Pauses workflow and notifies reviewer for click approval
   │
   ▼
[5. PRODUCTION Deployment Job]
   ├── Zero-Downtime Rolling Update on EKS 'gdp-production'
   ├── Run Production Smoke Verification
   └── Automatic Helm Rollback if Deployment Fails!
```

---

## ☸️ 8. Kubernetes Workloads & Auto-scaling

The Kubernetes application layer (`helm/gdp-prediction-app/` and `kubernetes/`) is configured with enterprise hardening standards:

1. **Security Context**:
   - `runAsNonRoot: true` (Runs under non-root UID `10001`).
   - `readOnlyRootFilesystem: true` (Prevents malware from writing to disk).
   - `allowPrivilegeEscalation: false`.
   - `capabilities: drop: ["ALL"]`.
2. **Autoscaling (HPA)**:
   - Scales API pods automatically between **2 (min)** and **15 (max)** based on CPU (75%) and Memory (80%) utilization.
3. **Pod Disruption Budget (PDB)**:
   - Enforces `minAvailable: 2` available replicas during cluster maintenance or node upgrades to guarantee zero downtime.
4. **Network Policies**:
   - Restricts pod egress traffic exclusively to PostgreSQL (5432), Redis (6379), HTTPS (443), and DNS (53).

---

## 📊 9. Observability, Metrics & Alerting

### Prometheus Metrics Exporter
The FastAPI application exposes native Prometheus metrics at `/metrics`:
- `http_requests_total`: Total HTTP requests partitioned by status code, method, and route.
- `http_request_duration_seconds`: Histogram measuring request latency bounds.

### Pre-Configured Prometheus Alert Rules (`monitoring/prometheus-rules.yaml`)
- **HighHTTPErrorRate**: Alerts if HTTP 5xx error rate exceeds 1% over 3 minutes.
- **HighLatencyP95**: Alerts if P95 request latency exceeds 500ms over 5 minutes.
- **PodCrashLooping**: Alerts if application pod restarts more than 2 times in 15 minutes.
- **DatabaseConnectionPoolHigh**: Alerts if PostgreSQL pool usage exceeds 80%.

### Grafana Dashboard (`monitoring/grafana-dashboard.json`)
Import `monitoring/grafana-dashboard.json` into Grafana (`http://localhost:3000`) to visualize real-time charts for:
- Request Rate (RPS)
- P95 / P99 Latency Histograms
- Pod CPU & Memory Utilization
- Model Inference Latencies

---

## 🔄 10. Disaster Recovery & Rollback Procedures

### RPO & RTO Objectives
- **Recovery Point Objective (RPO)**: `< 15 minutes` (AWS RDS automated backups & S3 object versioning).
- **Recovery Time Objective (RTO)**: `< 1 hour` (Automated IaC rebuild via Terraform).

### Automated Disaster Recovery Script (`scripts/disaster_recovery.sh`)
```bash
# 1. Create a manual RDS database snapshot and sync S3 model artifacts
./scripts/disaster_recovery.sh backup production

# 2. Trigger Disaster Recovery restore in failover environment
./scripts/disaster_recovery.sh restore production
```

### Manual Rollback Procedure
If a production release encounters runtime anomalies, rollback instantly using Helm:
```bash
# Update Kubeconfig
aws eks update-kubeconfig --region us-east-1 --name gdp-eks-production

# Roll back to previous working revision
helm rollback gdp-app-prod 0 --namespace gdp-production
```

---

## ❓ 11. Troubleshooting Guide

### Issue 1: Pod stuck in `CrashLoopBackOff`
- **Command**:
  ```bash
  kubectl logs -n gdp-production -l app.kubernetes.io/name=gdp-prediction-app --tail=100
  kubectl describe pod -n gdp-production -l app.kubernetes.io/name=gdp-prediction-app
  ```
- **Solution**: Verify database credentials in AWS Secrets Manager and check security group rules between EKS nodes and RDS.

### Issue 2: Terraform State Lock Error (`ConditionalCheckFailedException`)
- **Solution**: If a previous Terraform process crashed and left a stale lock in DynamoDB, force unlock:
  ```bash
  terraform force-unlock <LOCK_ID>
  ```

### Issue 3: Ingress Load Balancer Not Provisioning
- **Solution**: Ensure the AWS Load Balancer Controller is running in your EKS cluster and check controller logs:
  ```bash
  kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
  ```

---

## 📄 License & Attribution

This project is licensed under the **MIT License**.  
Designed and built for production engineering standards.
