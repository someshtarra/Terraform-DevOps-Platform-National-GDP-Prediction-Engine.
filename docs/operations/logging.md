# Centralized Logging Guide

## Log Structure
FastAPI application logs formatted in structured JSON:
```json
{
  "timestamp": "2026-08-25T20:30:00.000Z",
  "level": "INFO",
  "message": "GET /api/v1/forecast -> 200 (0.0120s)",
  "service": "gdp-prediction-service",
  "environment": "production",
  "correlation_id": "c8a1b2c3-d4e5-4f67-890a-bcdef1234567"
}
```

## CloudWatch Integration
Logs are streamed to CloudWatch Log Group `/aws/apps/gdp-prediction-production`.
