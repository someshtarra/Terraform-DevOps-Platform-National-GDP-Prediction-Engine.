# Architecture Overview — National GDP Prediction Platform

The National GDP Prediction Platform is a cloud-native, microservices-based machine learning prediction engine deployed on AWS EKS using Infrastructure as Code (Terraform).

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

## System Components
1. **Application Backend**: Python 3.11 FastAPI serving ARIMA + LSTM/GRU/CNN Hybrid GDP predictions.
2. **Infrastructure**: Provisioned via Terraform (`aws/`, `kubernetes/`, `github/`, `bootstrap/`).
3. **Database**: Managed AWS RDS PostgreSQL Multi-AZ cluster.
4. **Cache**: Managed AWS ElastiCache Redis cluster.
5. **Storage**: Amazon S3 bucket for model checkpoint storage.
