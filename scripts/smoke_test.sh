#!/usr/bin/env bash
set -e

ENV=${1:-dev}
echo "=========================================="
echo " Running Post-Deployment Smoke Tests ($ENV)"
echo "=========================================="

if [ "$ENV" == "dev" ]; then
    BASE_URL="http://localhost:8000"
elif [ "$ENV" == "staging" ]; then
    BASE_URL="https://gdp-staging.api.domain.com"
elif [ "$ENV" == "production" ]; then
    BASE_URL="https://gdp.api.domain.com"
else
    BASE_URL="http://localhost:8000"
fi

echo "[1/4] Checking Health Endpoint (/health)..."
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health")
if [ "$HEALTH_STATUS" -eq 200 ]; then
    echo "✔ Health check passed (HTTP 200)"
else
    echo "✖ Health check failed (HTTP $HEALTH_STATUS)"
    exit 1
fi

echo "[2/4] Checking Readiness Endpoint (/ready)..."
READY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/ready")
if [ "$READY_STATUS" -eq 200 ]; then
    echo "✔ Readiness check passed (HTTP 200)"
else
    echo "✖ Readiness check failed (HTTP $READY_STATUS)"
    exit 1
fi

echo "[3/4] Checking Latest GDP Endpoint (/api/v1/latest)..."
LATEST_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/latest")
if [ "$LATEST_STATUS" -eq 200 ]; then
    echo "✔ Latest GDP observation check passed (HTTP 200)"
else
    echo "✖ Latest GDP check failed (HTTP $LATEST_STATUS)"
    exit 1
fi

echo "[4/4] Checking ARIMA-LSTM Forecast Endpoint (/api/v1/forecast?quarters=4)..."
FORECAST_RES=$(curl -s "$BASE_URL/api/v1/forecast?quarters=4&model_type=ARIMA-LSTM")
if echo "$FORECAST_RES" | grep -q "ARIMA-LSTM"; then
    echo "✔ Model forecast output verified!"
else
    echo "✖ Forecast response verification failed!"
    echo "Response: $FORECAST_RES"
    exit 1
fi

echo "=========================================="
echo " ALL SMOKE TESTS PASSED SUCCESSFULLY! "
echo "=========================================="
