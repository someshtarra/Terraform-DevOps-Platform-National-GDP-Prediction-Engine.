# Disaster Recovery (DR) & Business Continuity Plan

## Objectives
- **Recovery Point Objective (RPO)**: < 15 minutes (Automated AWS RDS Point-in-Time Recovery & S3 Versioning).
- **Recovery Time Objective (RTO)**: < 1 hour (Automated Infrastructure as Code failover via Terraform & Helm).

## Failure Scenarios & Recovery Procedures

### 1. Database Failure (RDS Primary Unavailable)
- **Automatic Behavior**: In production, RDS Multi-AZ automatically detects primary instance failure and promotes the standby replica in < 60 seconds without changing DNS endpoints.
- **Manual Failover Command**:
  ```bash
  aws rds reboot-db-instance --db-instance-identifier gdp-postgres-production --force-failover
  ```

### 2. Kubernetes Cluster Failure (EKS Node Loss or Control Plane Degradation)
- **Recovery Action**:
  ```bash
  # Execute terraform to rebuild cluster
  cd terraform/environments/production
  terraform apply -auto-approve

  # Redeploy Helm chart
  ./scripts/disaster_recovery.sh restore production
  ```

### 3. Region Outage
- Re-run Terraform targeting secondary AWS region (e.g., `us-west-2`) using `scripts/disaster_recovery.sh restore production`.
