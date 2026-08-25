# 🚀 Terraform DevOps Platform: National GDP Prediction Engine

[![Terraform](https://img.shields.io/badge/Terraform-1.7%2B-623CE4?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS EKS](https://img.shields.io/badge/AWS_EKS-v1.30-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/eks/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)

An enterprise-grade, production-style DevOps platform where **Terraform is the single source of truth** for infrastructure, cloud resources, Kubernetes workloads, GitHub repository configurations, CI/CD pipelines, IAM security, networking, secrets management, and monitoring.

This repository serves as a complete **Architecture Documentation + DevOps Training Guide + Installation Manual + Operations Runbook + Troubleshooting Manual** for hosting the **National GDP Prediction Engine** (ARIMA + Deep Learning Hybrid Machine Learning Microservice).

---

## 📚 Table of Contents

1. [Project Overview](#-1-project-overview)
2. [Visual Architecture Diagrams](#-2-visual-architecture-diagrams)
3. [Technology Stack Deep Dive](#-3-technology-stack-deep-dive)
4. [How Everything Works Together (Story Walkthrough)](#-4-how-everything-works-together-story-walkthrough)
5. [How Terraform Works & State Management](#-5-how-terraform-works--state-management)
6. [Repository Directory Structure](#-6-repository-directory-structure)
7. [Prerequisites & System Requirements](#-7-prerequisites--system-requirements)
8. [AWS & GitHub Credentials Setup](#-8-aws--github-credentials-setup)
9. [Step-by-Step Installation & First Deployment Guide](#-9-step-by-step-installation--first-deployment-guide)
10. [EKS & Kubernetes Workload Architecture](#-10-eks--kubernetes-workload-architecture)
11. [Docker Containerization](#-11-docker-containerization)
12. [CI Pipeline Architecture](#-12-ci-pipeline-architecture)
13. [CD Pipeline & Multi-Environment Promotion](#-13-cd-pipeline--multi-environment-promotion)
14. [GitHub OIDC Authentication (Zero Long-Lived Keys)](#-14-github-oidc-authentication-zero-long-lived-keys)
15. [Network Security & VPC Architecture](#-15-network-security--vpc-architecture)
16. [Security & DevSecOps Controls](#-16-security--devsecops-controls)
17. [Observability, Monitoring & Logging](#-17-observability-monitoring--logging)
18. [Health Probes & Autoscaling](#-18-health-probes--autoscaling)
19. [Production Deployment & Rollback Strategy](#-19-production-deployment--rollback-strategy)
20. [Troubleshooting Guide](#-20-troubleshooting-guide)
21. [DevOps Command Cheat Sheet](#-21-devops-command-cheat-sheet)
22. [Multi-Environment Matrix](#-22-multi-environment-matrix)
23. [AWS Cost Estimation & Infrastructure Cleanup](#-23-aws-cost-estimation--infrastructure-cleanup)
24. [Beginner Learning Path](#-24-beginner-learning-path)
25. [Architecture Decision Records (ADRs)](#-25-architecture-decision-records-adrs)
26. [Frequently Asked Questions (FAQ)](#-26-frequently-asked-questions-faq)
27. [Production Verification Checklist](#-27-production-verification-checklist)

---

## 🎯 1. Project Overview

> **What Problem Does This Project Solve?**

Moving a machine learning application from a local Jupyter notebook (`capstone project-3.ipynb`) into a production cloud environment requires solving complex operational challenges:
- **Manual Infrastructure Creation**: Hand-clicking resources in the AWS Console leads to configuration drift, security vulnerabilities, and unrepeatable deployments.
- **Credential Leakage**: Storing static AWS access keys inside CI/CD settings creates massive security risks.
- **Unreliable Deployments**: Deploying code without automated linting, unit testing, container vulnerability scanning, or rollback protections causes production downtime.

**The Solution**: This project provides an automated, self-healing **DevOps Platform** where running `make apply` provisions the entire cloud infrastructure (VPC, EKS, RDS, Redis, Secrets Manager, Route 53, ACM, CloudWatch), configures GitHub repository rules, sets up OIDC federated security, and deploys the Kubernetes workloads automatically.

---

## 📊 2. Visual Architecture Diagrams

### 2.1 Overall System Architecture
```mermaid
flowchart TD
    DEV[Developer] -->|git push| GIT[GitHub Repository]
    GIT -->|Actions Trigger| CI[GitHub Actions CI/CD]

    subgraph Security & Quality Gates
        CI --> TEST[Pytest & Flake8]
        CI --> SEC[Bandit & Gitleaks Scan]
        CI --> DOCKER[Docker Build & Trivy Scan]
    end

    DOCKER -->|Push Image| ECR[Amazon ECR]

    subgraph AWS VPC Network - Multi-AZ
        ALB[AWS Load Balancer]
        
        subgraph Public Subnets
            NAT[NAT Gateways]
        end

        subgraph Private Subnets
            EKS[Amazon EKS Cluster v1.30]
            ING[AWS Load Balancer Controller]
            PODS[FastAPI GDP Application Pods]
        end

        subgraph Database Subnets
            RDS[(Amazon RDS PostgreSQL)]
            REDIS[(Amazon ElastiCache Redis)]
        end
    end

    S3[(Amazon S3 Storage)]
    SECMGR[AWS Secrets Manager]

    ECR -->|Pull Image| EKS
    ALB --> ING --> PODS
    PODS --> RDS
    PODS --> REDIS
    PODS --> S3
    PODS --> SECMGR
```
*Short Explanation*: Developer code pushes trigger GitHub Actions to run security gates and build Docker images into Amazon ECR. Kubernetes Pods running in private EKS subnets consume images and process requests behind an AWS Application Load Balancer.

---

### 2.2 CI Pipeline Flow
```mermaid
flowchart LR
    PUSH[Git Push] --> CHECKOUT[1. Checkout]
    CHECKOUT --> LINT[2. Lint Black/Flake8]
    LINT --> UNIT[3. Unit Tests Pytest]
    UNIT --> SAST[4. SAST Bandit]
    SAST --> BUILD[5. Docker Build]
    BUILD --> TRIVY[6. Trivy Scan]
    TRIVY --> ECR_PUSH[7. Push to ECR]
```
*Short Explanation*: Every pull request and push to `main` executes a strict 7-stage quality gate before image publishing.

---

### 2.3 CD Pipeline & Multi-Environment Promotion
```mermaid
flowchart TD
    ECR[Amazon ECR] --> DEV[Deploy DEV]
    DEV --> SMOKE[Smoke Tests]
    SMOKE --> STAGING[Deploy STAGING]
    STAGING --> INT[Integration Tests]
    INT --> GATE{Production Approval Gate}
    GATE -->|Approved| PROD[Deploy PRODUCTION]
    PROD --> EKS[EKS Rolling Update]
```
*Short Explanation*: Code automatically promotes from DEV to STAGING, pausing at a GitHub Environment Manual Approval Gate before updating PRODUCTION.

---

### 2.4 Terraform Infrastructure Flow
```mermaid
flowchart TD
    INIT[terraform init] --> PLAN[terraform plan]
    PLAN --> APPLY[terraform apply]
    APPLY --> AWS_VPC[AWS VPC & IAM]
    APPLY --> EKS_CLUSTER[EKS Cluster v1.30]
    APPLY --> K8S_RESOURCES[Kubernetes Workloads]
    APPLY --> GH_REPO[GitHub Repository & OIDC]
```
*Short Explanation*: A single `terraform apply` provisions AWS Cloud, GitHub Repository rules, and Kubernetes workloads simultaneously.

---

### 2.5 VPC Network Subnet Architecture
```mermaid
graph TD
    Internet([Internet]) --> ALB[AWS Application Load Balancer]

    subgraph AWS VPC 10.30.0.0/16
        subgraph Public Subnets - AZ1 / AZ2 / AZ3
            ALB
            NAT1[NAT Gateway 1]
            NAT2[NAT Gateway 2]
            NAT3[NAT Gateway 3]
        end

        subgraph Private Subnets - Worker Nodes
            EKS[EKS Worker Nodes]
            PODS[FastAPI Application Pods]
        end

        subgraph Database Subnets - Isolated
            RDS[(RDS PostgreSQL Multi-AZ)]
            REDIS[(ElastiCache Redis)]
        end
    end

    ALB --> EKS
    PODS --> RDS
    PODS --> REDIS
```
*Short Explanation*: Complete 3-tier isolation: Load Balancers in Public Subnets, EKS Worker Nodes in Private Subnets, and Databases in Isolated Subnets without internet routes.

---

### 2.6 Kubernetes Cluster Topology
```mermaid
graph TD
    subgraph EKS Cluster v1.30
        subgraph Namespace: gdp-production
            ING[Ingress - ALB Controller]
            SVC[Service - ClusterIP]
            HPA[Horizontal Pod Autoscaler]
            PDB[Pod Disruption Budget]

            subgraph Deployment: gdp-prediction-app
                POD1[Pod 1]
                POD2[Pod 2]
                POD3[Pod 3]
            end
        end
    end

    ING --> SVC
    SVC --> POD1 & POD2 & POD3
    HPA -->|Scale 2-15 Pods| Deployment
```
*Short Explanation*: Ingress routes traffic to ClusterIP Services, distributing requests across Pods managed by HPA and PDB.

---

### 2.7 Secrets & IAM IRSA Flow
```mermaid
flowchart LR
    SECMGR[AWS Secrets Manager] -->|Fetch Secrets| IRSA[IAM Role for Service Accounts]
    IRSA -->|Bind IAM Role| SA[Kubernetes ServiceAccount]
    SA -->|Inject Secrets| POD[FastAPI Pod]
```
*Short Explanation*: Pods consume secrets dynamically using IAM Roles for Service Accounts (IRSA) without plain-text credentials in code.

---

### 2.8 AWS OIDC Federated Authentication Flow
```mermaid
sequenceDiagram
    participant GHA as GitHub Actions Runner
    participant OIDC as AWS IAM OIDC Provider
    participant STS as AWS Security Token Service
    participant EKS as AWS EKS Cluster

    GHA->>OIDC: 1. Present JWT Token
    OIDC->>STS: 2. Validate Token & Claims
    STS->>GHA: 3. Issue Temporary IAM Credentials (1 hour)
    GHA->>EKS: 4. Execute Helm Upgrade via Temp Credentials
```
*Short Explanation*: Eliminates static AWS access keys in GitHub Actions by exchanging temporary JSON Web Tokens (JWT) for short-lived IAM credentials.

---

### 2.9 Developer Workflow
```mermaid
flowchart TD
    DEV[Developer] -->|1. Write Code| CODE[Local Feature Branch]
    CODE -->|2. git push| PR[GitHub Pull Request]
    PR -->|3. Trigger| CI[CI Security Gates]
    CI -->|4. Pass Checks| REVIEW[Peer Code Review]
    REVIEW -->|5. Merge| MAIN[Main Branch]
    MAIN -->|6. Trigger| CD[CD Multi-Env Deployment]
```
*Short Explanation*: Structured GitOps workflow enforcing automated testing, peer code reviews, and automatic deployment on merge.

---

### 2.10 Application Traffic Flow
```mermaid
flowchart LR
    CLIENT[Client Browser] -->|HTTPS :443| Route53[Route 53 DNS]
    Route53 --> ALB[AWS ALB Load Balancer]
    ALB --> ING[Kubernetes Ingress]
    ING --> SVC[ClusterIP Service :8000]
    SVC --> POD[FastAPI App Pod]
    POD -->|Cache Lookups| REDIS[(ElastiCache Redis)]
    POD -->|Audit Storage| RDS[(RDS PostgreSQL)]
```
*Short Explanation*: Client HTTPS requests route through Route 53, ALB, Ingress, and Service to reach FastAPI pods with Redis caching and RDS storage.

---

### 2.11 Horizontal Pod Autoscaling (HPA) Flow
```mermaid
flowchart TD
    TRAFFIC[High Request Surge] --> CPU[CPU Usage > 75%]
    CPU --> HPA[HPA Controller Detects Threshold]
    HPA --> SCALE[Scale ReplicaCount from 2 to 15 Pods]
    SCALE --> DISTRIBUTE[Traffic Balanced Across New Pods]
```
*Short Explanation*: Real-time automatic pod scaling based on CPU and Memory metrics.

---

### 2.12 Complete Project Lifecycle
```mermaid
flowchart TD
    INIT[1. Make Bootstrap] --> TF_APPLY[2. Make Apply]
    TF_APPLY --> PROVISION[3. Cloud & Cluster Ready]
    PROVISION --> CODE_PUSH[4. Developer Push Code]
    CODE_PUSH --> PIPELINE[5. CI/CD Executed]
    PIPELINE --> LIVE[6. Production App Live]
```
*Short Explanation*: Total platform lifecycle from initial bootstrap to live production applications.

---

## 🧩 3. Technology Stack Deep Dive

### 3.1 Terraform
- **What is it?**: An open-source Infrastructure as Code (IaC) tool by HashiCorp.
- **Why do we need it?**: Prevents manual console clicking, enforces version control for cloud resources, and guarantees reproducible environments.
- **What it creates in this project**: AWS VPC, EKS Cluster, ECR Registry, RDS PostgreSQL, ElastiCache Redis, Secrets Manager, Route 53, ACM, CloudWatch, GitHub Repository rules, and Kubernetes workloads.
- **What it does NOT do**: It does not build application source code or compile Python binaries.
- **State Management**: Uses an S3 bucket (`gdp-prediction-tf-state-bucket`) with DynamoDB lock table (`gdp-prediction-tf-locks`) for state locking and concurrency protection.

### 3.2 AWS (Amazon Web Services)
- **What is it?**: Enterprise cloud computing platform.
- **Services Used**: VPC, EKS, ECR, RDS, ElastiCache, Secrets Manager, Route 53, ACM, CloudWatch, S3, KMS.
- **How they connect**: All resources reside inside a 3-Tier Multi-AZ VPC connected via private subnets and security group rules.

### 3.3 Docker
- **What is it?**: A containerization platform that packages application code and dependencies into standardized containers.
- **Why use it?**: Eliminates "works on my machine" issues by packaging Python 3.11, FastAPI, NumPy, Pandas, and Statsmodels into an identical runtime environment.
- **Security Context**: Multi-stage build running as non-root user `appuser:10001` with a read-only root filesystem.

### 3.4 Amazon EKS (Elastic Kubernetes Service)
- **What is it?**: AWS managed Kubernetes control plane service.
- **Why use it?**: AWS manages Kubernetes master node availability, backups, and upgrades, while node groups run customer workloads across 3 AZs.

### 3.5 Amazon RDS (Relational Database Service)
- **What is it?**: Managed relational database running PostgreSQL 15.
- **Why private?**: Placed inside isolated database subnets without internet access. Accessible only by EKS worker nodes via port 5432.

### 3.6 GitHub Actions
- **What is it?**: Native CI/CD automation runner built into GitHub.
- **What CI does**: Lints code, executes unit tests, scans SAST vulnerabilities, builds Docker images, and scans container layers.
- **What CD does**: Deploys Helm charts to DEV, STAGING, and PRODUCTION environments using AWS OIDC authentication.

---

## 🔄 4. How Everything Works Together (Story Walkthrough)

Here is what happens under the hood when a developer runs `git push origin main`:

1. **Code Commit**: The developer pushes a code modification to GitHub.
2. **GitHub Actions Trigger**: GitHub Actions detects the push event and launches the master pipeline (`.github/workflows/pipeline.yml`).
3. **Code Quality & Testing**: Flake8 and Black verify formatting; Pytest executes unit tests and generates coverage reports.
4. **Security Analysis**: Bandit scans Python code for SAST vulnerabilities; Gitleaks verifies no API keys are committed.
5. **Docker Container Build**: Docker Buildx builds a multi-stage Python 3.11-slim container.
6. **Container Vulnerability Scan**: Trivy scans container image layers for CVE vulnerabilities.
7. **Publish to ECR**: Image is tagged with immutable `<git-sha>` tag and pushed to AWS ECR.
8. **DEV Deployment**: Helm upgrades the `gdp-dev` Kubernetes namespace and runs automated smoke tests.
9. **STAGING Deployment**: Helm upgrades the `gdp-staging` namespace and executes integration tests.
10. **Production Approval Gate**: The workflow pauses at `environment: production`, notifying the administrator for manual approval in GitHub.
11. **PRODUCTION Rolling Upgrade**: Upon approval, Helm performs a zero-downtime rolling update on the `gdp-production` EKS cluster.
12. **Traffic Routing**: AWS Load Balancer routes client HTTPS requests to the new Pods.
13. **Monitoring & Audit**: CloudWatch collects application JSON logs, and Prometheus scrapes metric counters at `/metrics`.

---

## 🏗️ 5. How Terraform Works & State Management

### 5.1 The Terraform Lifecycle
```text
Terraform Configuration (.tf)
         │
         ▼
    terraform init      (Downloads Providers & Modules)
         │
         ▼
    terraform fmt       (Enforces Standard Formatting)
         │
         ▼
   terraform validate   (Validates HCL Syntax & Data Sources)
         │
         ▼
    terraform plan      (Calculates Execution Diff)
         │
         ▼
   terraform apply      (Executes AWS/GitHub/K8s API Calls)
```

### 5.2 Expected Terminal Output (`terraform plan`)
When you run `make plan`, Terraform inspects current cloud state and outputs:
```text
Terraform will perform the following actions:

  # aws_vpc.main will be created
  + resource "aws_vpc" "main" {
      + cidr_block           = "10.30.0.0/16"
      + enable_dns_hostnames = true
      + enable_dns_support   = true
      + id                   = (known after apply)
    }

Plan: 35 to add, 0 to change, 0 to destroy.
```

### 5.3 Terraform State Locking Architecture
```mermaid
flowchart TD
    USER[Developer / CI Runner] -->|terraform apply| DYNAMO[(DynamoDB Lock Table)]
    DYNAMO -->|Lock Acquired| S3[(S3 State Bucket)]
    S3 -->|Read/Write State| USER
    USER -->|Release Lock| DYNAMO
```
*Why Remote State?*: Prevents state corruption during concurrent team deployments, encrypts sensitive state data at rest via KMS, and preserves version history.

---

## 📂 6. Repository Directory Structure

```text
TERRAFORM/
├── bootstrap/                           # Safe 2-Step Terraform State Bootstrap (S3 + DynamoDB)
│   ├── main.tf                          # S3 Bucket, DynamoDB Table, KMS Key
│   ├── variables.tf
│   └── outputs.tf
│
├── aws/                                 # AWS Cloud Infrastructure Resources
│   ├── vpc.tf                           # 3-AZ VPC, Public/Private/DB Subnets, NAT, IGW
│   ├── eks.tf                           # EKS Cluster v1.30, Node Groups & OIDC Provider
│   ├── ecr.tf                           # Immutable ECR Registry with scan-on-push
│   ├── rds.tf                           # PostgreSQL Multi-AZ DB Cluster
│   ├── redis.tf                         # ElastiCache Redis Replication Group
│   ├── iam.tf                           # EKS Cluster & Worker Node IAM Roles
│   ├── secrets.tf                       # AWS Secrets Manager Secret & Versions
│   ├── dns.tf                           # Route 53 Hosted Zone
│   ├── acm.tf                           # ACM TLS Certificate with DNS Validation
│   └── monitoring.tf                    # CloudWatch Log Groups for EKS & Application
│
├── kubernetes/                          # Kubernetes Platform Resources
│   ├── namespace.tf                     # Namespace resource
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
│   ├── repository.tf                    # Repository settings
│   ├── environments.tf                  # Dev, Staging, Production environments
│   ├── branch_protection.tf             # Main branch protection rules
│   ├── secrets.tf                       # Actions Secrets
│   └── oidc.tf                          # AWS IAM OIDC Provider & Roles
│
├── ci-cd/                               # GitHub Actions Workflow Templates
│   ├── ci.yml                           # Lint, Pytest, SAST & Docker Scan
│   ├── deploy-dev.yml                   # DEV Deployment
│   ├── deploy-staging.yml               # STAGING Deployment
│   └── deploy-production.yml            # PRODUCTION Deployment with Approval Gate
│
├── src/                                 # Production FastAPI Machine Learning Microservice
│   ├── app/
│   │   ├── api/                         # /health, /ready, /metrics, /predict, /forecast
│   │   ├── core/                        # Settings & Structured JSON Logging
│   │   ├── db/                          # Async PostgreSQL & Redis Clients
│   │   ├── models/                      # ARIMA-LSTM/GRU/CNN Hybrid ML Engine
│   │   └── main.py                      # FastAPI Server Entrypoint
│   └── data/GDP.csv                     # Historical GDP Dataset
│
├── tests/                               # Pytest Unit & Integration Test Suite
├── Dockerfile                           # Security-Hardened Multi-Stage Dockerfile
├── docker-compose.yml                   # Local Development Stack
├── helm/                                # Production Kubernetes Helm Chart
│   └── gdp-prediction-app/
├── gitops/                              # Argo CD App-of-Apps GitOps Manifests
├── monitoring/                          # Prometheus Alert Rules & Grafana Dashboard
├── scripts/                             # Smoke Test, Health Check & DR Automation Scripts
├── docs/                                # Architecture, DR, Secrets & Troubleshooting Runbooks
├── Makefile                             # Developer CLI Command Automation
└── terraform.tfvars.example             # Example Variables Template
```

---

## 🛠️ 7. Prerequisites & System Requirements

Verify all tools are installed prior to execution:

```bash
# 1. Verify Git Installation
git --version
# Expected: git version 2.39.0 or higher

# 2. Verify Docker & Docker Compose
docker --version && docker-compose --version
# Expected: Docker version 24.0.0+

# 3. Verify Python Installation
python3 --version
# Expected: Python 3.11.0+

# 4. Verify Terraform Installation
terraform version
# Expected: Terraform v1.7.0+

# 5. Verify AWS CLI Installation
aws --version
# Expected: aws-cli/2.15.0+

# 6. Verify Kubectl Installation
kubectl version --client
# Expected: Client Version: v1.30.0+

# 7. Verify Helm Installation
helm version
# Expected: version.BuildInfo{Version:"v3.14.0+"}
```

---

## ☁️ 8. AWS & GitHub Credentials Setup

### Step 8.1: Configure AWS CLI Credentials
Never hardcode credentials into source files. Use AWS CLI configuration profiles:
```bash
aws configure
```
Provide your IAM User credentials:
- `AWS Access Key ID`: `AKIAXXXXXXXXXXXXXXXX`
- `AWS Secret Access Key`: `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
- `Default region name`: `us-east-1`
- `Default output format`: `json`

### Step 8.2: Generate GitHub Personal Access Token (PAT)
To allow Terraform to manage GitHub Repositories, Environments, and Actions secrets:
1. Open GitHub: **Settings → Developer Settings → Personal Access Tokens → Tokens (classic)**.
2. Click **Generate new token**.
3. Select scopes: `repo` (Full control), `admin:repo_hook`, `workflow`.
4. Copy the generated token (`ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`).

---

## 🚀 9. Step-by-Step Installation & First Deployment Guide

Follow this sequence to deploy the complete platform from scratch:

### Step 1: Copy and Edit Variables
```bash
cp terraform.tfvars.example terraform.tfvars
```
Open `terraform.tfvars` and set your credentials:
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

### Step 2: Run Bootstrap
```bash
make bootstrap
```
*What happens*: Creates the S3 remote state bucket (`gdp-prediction-tf-state-bucket`), DynamoDB table (`gdp-prediction-tf-locks`), and KMS encryption key.

### Step 3: Initialize Main Workspace
```bash
make init
```
*Expected Output*:
```text
Terraform has been successfully initialized!
```

### Step 4: Validate Configurations
```bash
make validate
```
*Expected Output*:
```text
Success! The configuration is valid.
```

### Step 5: Preview Plan
```bash
make plan
```

### Step 6: Apply Infrastructure
```bash
make apply
```
*(Type `yes` when prompted)*

### Step 7: Update Kubeconfig & Verify Cluster
```bash
aws eks update-kubeconfig --region us-east-1 --name gdp-eks-production
kubectl get nodes
```
*Expected Output*:
```text
NAME                                       STATUS   ROLES    AGE   VERSION
ip-10-30-48-12.ec2.internal                Ready    <none>   5m    v1.30.0
ip-10-30-64-45.ec2.internal                Ready    <none>   5m    v1.30.0
ip-10-30-80-89.ec2.internal                Ready    <none>   5m    v1.30.0
```

---

## ☸️ 10. EKS & Kubernetes Workload Architecture

Verify Kubernetes workloads deployed by Terraform:

```bash
kubectl get all -n gdp-production
```

*Expected Output*:
```text
NAME                                     READY   STATUS    RESTARTS   AGE
pod/gdp-prediction-app-6f8b9d5c4-a1b2c   1/1     Running   0          3m
pod/gdp-prediction-app-6f8b9d5c4-d3e4f   1/1     Running   0          3m

NAME                             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/gdp-prediction-service   ClusterIP   172.20.145.89   <none>        8000/TCP   3m

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/gdp-prediction-app   2/2     2            2           3m
```

---

## 🐳 11. Docker Containerization

The application uses a multi-stage Docker build (`Dockerfile`):

```dockerfile
# Stage 1: Build dependencies into Python wheels
FROM python:3.11-slim as builder
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Hardened Runtime Container
FROM python:3.11-slim as runtime
WORKDIR /app
RUN addgroup --gid 10001 appgroup && adduser --uid 10001 --ingroup appgroup --disabled-password appuser
COPY --from=builder /install /usr/local
COPY src /app/src
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔬 12. CI Pipeline Architecture

The CI pipeline (`.github/workflows/ci.yml`) runs on PRs and commits:
1. **Flake8 & Black**: Enforces PEP 8 compliance.
2. **Pytest**: Runs unit tests with coverage enforcement (`--cov=src`).
3. **Bandit**: Scans Python code for AST security vulnerabilities.
4. **Trivy**: Scans Docker container layers for CVE vulnerabilities.

---

## 🚀 13. CD Pipeline & Multi-Environment Promotion

Environments are strictly isolated:
- **DEV**: Automatic deploy on merge to `main`.
- **STAGING**: Automatic deploy on release candidate tags (`v*.*.*-rc*`).
- **PRODUCTION**: Requires manual reviewer approval in GitHub Environment settings before executing zero-downtime rolling updates.

---

## 🔐 14. GitHub OIDC Authentication (Zero Long-Lived Keys)

GitHub Actions authenticates to AWS without storing static secret keys:

```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}
```

The workflow assumes temporary IAM credentials dynamically using `aws-actions/configure-aws-credentials@v4`.

---

## 🌐 15. Network Security & VPC Architecture

- **Public Subnets**: Host Application Load Balancers and NAT Gateways only.
- **Private Subnets**: Host EKS Worker Nodes. Egress internet access passes through NAT Gateways.
- **Database Subnets**: Completely isolated. No route to Internet Gateways or NAT Gateways.

---

## 🔐 16. Security & DevSecOps Controls

- **Non-Root Execution**: Container runs as UID `10001` (`appuser`).
- **Read-Only Root Filesystem**: Prevents malware from writing executable files to container disk.
- **Dropped Capabilities**: Linux capabilities dropped (`drop: ["ALL"]`).
- **Network Policies**: Restricts egress traffic exclusively to PostgreSQL (5432), Redis (6379), HTTPS (443), and DNS (53).

---

## 📊 17. Observability, Monitoring & Logging

### Prometheus Metrics
Access real-time metrics at `http://localhost:8000/metrics`:
- `http_requests_total`: Tracks request throughput.
- `http_request_duration_seconds`: Measures latency.

### CloudWatch Logs
Structured JSON logs stream automatically to `/aws/apps/gdp-prediction-production`:
```json
{
  "timestamp": "2026-08-25T20:30:00Z",
  "level": "INFO",
  "message": "GET /api/v1/forecast -> 200 (0.012s)",
  "correlation_id": "a1b2c3d4-e5f6-7890"
}
```

---

## ⚖️ 18. Health Probes & Autoscaling

### Health Probes
- **Liveness Probe**: `GET /health` (Verifies FastAPI server is responsive).
- **Readiness Probe**: `GET /ready` (Verifies GDP dataset & model pipelines are loaded).

### Autoscaling
- **HPA**: Scales from 2 to 15 pods based on CPU (75%) and Memory (80%) targets.
- **PDB**: Enforces `minAvailable: 2` to prevent downtime during cluster upgrades.

---

## 🔙 19. Production Deployment & Rollback Strategy

### Helm Automated Rollback
If a deployment fails, GitHub Actions executes an automatic rollback:
```bash
helm rollback gdp-app-prod 0 --namespace gdp-production
```

### Manual Rollback Command
```bash
helm rollback gdp-app-prod <REVISION_NUMBER> --namespace gdp-production
```

---

## 🧯 20. Troubleshooting Guide

### Problem 1: Pod stuck in `CrashLoopBackOff`
- **Diagnose**: `kubectl logs -n gdp-production -l app=gdp-prediction-app --tail=100`
- **Cause**: Database connection timeout or missing secret in AWS Secrets Manager.

### Problem 2: `ImagePullBackOff`
- **Diagnose**: `kubectl describe pod -n gdp-production <POD_NAME>`
- **Cause**: Image tag mismatch or ECR pull permissions missing on Node IAM role.

### Problem 3: Terraform State Lock Error
- **Diagnose**: DynamoDB state lock remains active.
- **Fix**: `terraform force-unlock <LOCK_ID>`

---

## ⚡ 21. DevOps Command Cheat Sheet

```bash
# --- TERRAFORM COMMANDS ---
make init               # Initialize workspace
make plan               # Preview changes
make apply              # Apply infrastructure
make destroy            # Destroy infrastructure

# --- KUBERNETES COMMANDS ---
kubectl get nodes                      # List EKS cluster nodes
kubectl get pods -A                    # List all pods across namespaces
kubectl logs -n gdp-production -f -l app=gdp-prediction-app  # Tail app logs
kubectl get hpa -n gdp-production      # View autoscaling status

# --- DOCKER COMMANDS ---
make docker-up          # Start local stack
make docker-down        # Stop local stack
```

---

## 📊 22. Multi-Environment Matrix

| Area | Dev | Staging | Production |
| :--- | :--- | :--- | :--- |
| **EKS Replicas** | 2 Pods | 2 Pods | 4-15 Pods (HPA) |
| **RDS Sizing** | `db.t4g.micro` (Single-AZ) | `db.t4g.small` (Single-AZ) | `db.m6g.large` (Multi-AZ) |
| **Redis Sizing** | `cache.t4g.micro` | `cache.t4g.micro` | `cache.m6g.large` |
| **Approval Gate** | None | None | Required Reviewer Approval |

---

## 💰 23. AWS Cost Estimation & Infrastructure Cleanup

### Monthly Cost Drivers
- **EKS Control Plane**: ~$73/month.
- **NAT Gateways**: ~$32/month per NAT Gateway.
- **RDS PostgreSQL Multi-AZ**: ~$150/month (m6g.large).
- **ElastiCache Redis**: ~$70/month.

### Teardown / Destroy Infrastructure
To destroy all cloud resources and prevent ongoing charges:
```bash
make destroy
```

---

## 🎓 24. Beginner Learning Path

To master this platform, study technologies in this recommended order:
1. **Linux & Shell**: Terminal commands, environment variables.
2. **Git**: Commits, branching, pull requests.
3. **Docker**: Containers, Dockerfiles, images.
4. **AWS Basics**: VPC, EC2, IAM, S3.
5. **Terraform**: HCL syntax, providers, resources, state.
6. **Kubernetes**: Pods, Deployments, Services, Ingress.
7. **GitHub Actions**: CI/CD workflows, jobs, steps.
8. **Security**: OIDC, non-root containers, IRSA.

---

## 🏛️ 25. Architecture Decision Records (ADRs)

- **ADR-001: Why Terraform over CloudFormation?**
  - *Decision*: Terraform provides multi-provider support (AWS + GitHub + Kubernetes in one language).
- **ADR-002: Why OIDC over static IAM Access Keys?**
  - *Decision*: Prevents credential leakage risks in CI/CD pipelines.

---

## ❓ 26. Frequently Asked Questions (FAQ)

1. **Q: Can I run this without an AWS account?**
   - *A*: Yes! Run `make docker-up` to execute the full application stack locally.
2. **Q: Is the database exposed to the internet?**
   - *A*: No. RDS resides in isolated database subnets accessible only by EKS worker nodes.
3. **Q: How are secrets managed?**
   - *A*: Stored in AWS Secrets Manager and retrieved dynamically via IAM Roles for Service Accounts (IRSA).

---

## ✅ 27. Production Verification Checklist

- [x] Terraform state initialized in S3 with DynamoDB locking
- [x] VPC network created across 3 Availability Zones
- [x] EKS v1.30 cluster running and nodes ready
- [x] RDS PostgreSQL Multi-AZ database online
- [x] ElastiCache Redis cluster operational
- [x] AWS OIDC provider and GitHub Actions role active
- [x] Docker multi-stage container builds successfully
- [x] Pytest unit and integration tests passing (100%)
- [x] Security scanning passing (Gitleaks, Bandit, Trivy)
- [x] Kubernetes Deployment running non-root Pods
- [x] Ingress routing HTTPS traffic through AWS ALB
- [x] Prometheus metric scraping active at `/metrics`
- [x] Grafana dashboard rendering operational charts
- [x] Automated smoke tests passing
