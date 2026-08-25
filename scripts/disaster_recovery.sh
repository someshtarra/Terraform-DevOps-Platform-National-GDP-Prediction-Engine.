#!/usr/bin/env bash
set -e

ACTION=${1:-backup}
ENV=${2:-production}

echo "=================================================="
echo " AWS Disaster Recovery Execution Script ($ACTION - $ENV)"
echo "=================================================="

if [ "$ACTION" == "backup" ]; then
    echo "[1] Creating Manual AWS RDS Snapshot..."
    SNAPSHOT_ID="gdp-rds-manual-snap-$(date +%Y%m%d%H%M%S)"
    aws rds create-db-snapshot \
        --db-instance-identifier "gdp-postgres-$ENV" \
        --db-snapshot-identifier "$SNAPSHOT_ID"
    echo "✔ RDS Snapshot created: $SNAPSHOT_ID"

    echo "[2] Syncing S3 Model Artifacts to Secondary Disaster Recovery Bucket..."
    aws s3 sync "s3://gdp-prediction-models-$ENV" "s3://gdp-prediction-models-$ENV-dr-backup"
    echo "✔ S3 DR Sync Complete."

elif [ "$ACTION" == "restore" ]; then
    echo "[!] WARNING: TRIGGERING DISASTER RECOVERY RESTORE PROCEDURE..."
    echo "[1] Redeploying Terraform Infrastructure in Failover Region..."
    cd terraform/environments/"$ENV"
    terraform init
    terraform apply -auto-approve

    echo "[2] Re-pointing Helm Release to Restored Cluster..."
    aws eks update-kubeconfig --region us-east-1 --name "gdp-eks-$ENV"
    helm upgrade --install gdp-app-prod ./helm/gdp-prediction-app \
        --namespace "gdp-$ENV" --create-namespace \
        --values ./helm/gdp-prediction-app/values-"$ENV".yaml

    echo "✔ Disaster Recovery Restoration Sequence Complete."
else
    echo "Usage: ./scripts/disaster_recovery.sh [backup|restore] [dev|staging|production]"
    exit 1
fi
