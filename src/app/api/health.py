from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
from app.models.hybrid_engine import gdp_engine
from app.core.config import settings

router = APIRouter(tags=["Health & Monitoring"])

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP Request Latency", ["endpoint"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENV,
    }


@router.get("/ready")
async def readiness_check():
    is_ready = gdp_engine.is_loaded
    if is_ready:
        return {"status": "ready", "dataset_loaded": True}
    return Response(content='{"status": "not_ready"}', status_code=503, media_type="application/json")


@router.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
