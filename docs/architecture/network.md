# VPC Network Architecture

The network infrastructure is designed with strict security isolation across 3 Availability Zones (AZs).

```mermaid
graph TD
    Internet([Internet Traffic]) --> ALB[AWS Application Load Balancer]

    subgraph AWS VPC 10.30.0.0/16
        subgraph Public Subnets - 10.30.0.0/20, 10.30.16.0/20, 10.30.32.0/20
            ALB
            IGW[Internet Gateway]
            NAT1[NAT Gateway AZ1]
            NAT2[NAT Gateway AZ2]
            NAT3[NAT Gateway AZ3]
        end

        subgraph Private Subnets - 10.30.48.0/20, 10.30.64.0/20, 10.30.80.0/20
            EKS[EKS Worker Nodes]
            PODS[Application Pods]
        end

        subgraph Isolated Database Subnets - 10.30.96.0/20, 10.30.112.0/20, 10.30.128.0/20
            RDS[(RDS PostgreSQL)]
            REDIS[(ElastiCache Redis)]
        end
    end

    ALB --> EKS
    PODS --> RDS
    PODS --> REDIS
```

## Network Security Controls
- **Public Subnets**: Contain Load Balancers and NAT Gateways only.
- **Private Subnets**: Contain EKS worker nodes; outbound internet traffic routes through NAT Gateways.
- **Database Subnets**: Completely isolated without internet access. Egress/Ingress restricted to EKS node security groups.
