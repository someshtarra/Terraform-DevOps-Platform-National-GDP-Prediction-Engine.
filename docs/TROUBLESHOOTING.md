# Operations & Troubleshooting Guide

## Common Incident Scenarios

### 1. Pods in `CrashLoopBackOff`
- **Diagnose**:
  ```bash
  kubectl logs -n gdp-production -l app.kubernetes.io/name=gdp-prediction-app --tail=100
  kubectl describe pod -n gdp-production -l app.kubernetes.io/name=gdp-prediction-app
  ```
- **Likely Root Cause**: Database or Redis connectivity timeout, missing configuration environment variable.

### 2. High Request Latency (>500ms)
- **Diagnose**: Check Grafana dashboard for cache hit ratio.
- **Remediation**: Verify Redis cluster health and ensure `REDIS_HOST` is accessible.

### 3. Deployment Stuck / Pending Pods
- **Diagnose**: Check node capacity (`kubectl describe nodes`) or quota limits.
- **Remediation**: Scale up node group via Terraform or adjust resource requests in `values-production.yaml`.
