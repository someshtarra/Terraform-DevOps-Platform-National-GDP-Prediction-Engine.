# Application & Infrastructure Rollback Guide

## Application Rollback (Helm)
```bash
# View deployment revision history
helm history gdp-app-prod -n gdp-production

# Roll back to target revision (e.g. revision 12)
helm rollback gdp-app-prod 12 -n gdp-production
```

## Infrastructure Rollback (Terraform)
Re-apply previous Git tag state:
```bash
git checkout v1.0.0
cd terraform
terraform init
terraform plan
terraform apply
```
