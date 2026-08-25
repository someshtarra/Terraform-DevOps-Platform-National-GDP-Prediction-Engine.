# Secrets Management Strategy

## Guiding Principles
- **No Hardcoded Secrets**: Zero plain-text credentials in Git, Dockerfiles, or Helm manifests.
- **Least Privilege Access**: Pods obtain AWS credentials dynamically via IRSA (IAM Roles for Service Accounts).

## Production Solution
1. **AWS Secrets Manager**: Database passwords, Redis auth tokens, and API credentials stored in AWS Secrets Manager.
2. **External Secrets Operator (ESO)**: Kubernetes operator synchronizes AWS Secrets Manager keys directly into native Kubernetes `Secret` resources in the application namespace.
3. **Local Development**: `.env` files injected via `docker-compose.yml` (never committed to repository).
