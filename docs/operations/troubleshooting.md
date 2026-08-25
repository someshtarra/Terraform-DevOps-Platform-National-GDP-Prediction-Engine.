# Operations Troubleshooting Manual

## Common Diagnostic Commands

### 1. Check Pod Status & Logs
```bash
kubectl get pods -n gdp-production
kubectl logs -n gdp-production -l app=gdp-prediction-app --tail=100
kubectl describe pod -n gdp-production -l app=gdp-prediction-app
```

### 2. Check Ingress & Service Status
```bash
kubectl get ingress -n gdp-production
kubectl describe ingress gdp-prediction-ingress -n gdp-production
```

### 3. Release DynamoDB Terraform Lock
```bash
terraform force-unlock <LOCK_ID>
```
