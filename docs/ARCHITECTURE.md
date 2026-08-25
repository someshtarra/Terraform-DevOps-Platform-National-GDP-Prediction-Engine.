# System Architecture & Infrastructure Design

## Overview
The National GDP Prediction Platform is a cloud-native, microservice-based machine learning forecasting engine deployed on Amazon Web Services (AWS) using Amazon EKS (Kubernetes v1.30).

```mermaid
graph TD
    User([Client / Consumer]) -->|HTTPS / SSL| ALB[AWS Application Load Balancer]
    
    subgraph AWS VPC (10.30.0.0/16 - Production)
        subgraph Public Subnets
            ALB
            NAT[NAT Gateways]
        end

        subgraph Private Subnets (EKS Cluster)
            ING[ALB Ingress Controller]
            POD1[FastAPI Pod - Pod 1]
            POD2[FastAPI Pod - Pod 2]
            POD3[FastAPI Pod - Pod 3]
            HPA[Horizontal Pod Autoscaler]
        end

        subgraph Isolated Database Subnets
            RDS[(AWS RDS PostgreSQL Multi-AZ)]
            REDIS[(AWS ElastiCache Redis Cluster)]
        end
    end

    S3[(AWS S3 Model Artifact Bucket)]

    ALB --> ING
    ING --> POD1 & POD2 & POD3
    POD1 & POD2 & POD3 --> RDS
    POD1 & POD2 & POD3 --> REDIS
    POD1 & POD2 & POD3 --> S3
```

## Core Components
1. **Application Backend**: Python 3.11 FastAPI server serving hybrid ARIMA-LSTM / ARIMA-GRU / ARIMA-CNN model predictions.
2. **Database Layer**: AWS RDS PostgreSQL (Multi-AZ in production) storing prediction metadata, query histories, and audit logs.
3. **Caching Layer**: AWS ElastiCache Redis Replication Group caching model forecast outputs with 1-hour TTL.
4. **Storage Layer**: AWS S3 Bucket storing serialized deep learning weight checkpoints and datasets.
5. **Ingress & Networking**: AWS Load Balancer Controller managing external HTTPS ALB traffic routing into internal Kubernetes Service ClusterIPs.
