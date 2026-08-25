from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from app.models.hybrid_engine import gdp_engine
from app.db.redis_client import get_cache, set_cache
from app.core.logging import logger

router = APIRouter(prefix="/api/v1", tags=["GDP Predictions & Forecasts"])


class ForecastResponse(BaseModel):
    status: str
    quarters_requested: int
    model_type: str
    latest_gdp: dict
    forecasts: list


@router.get("/latest", summary="Get Latest Historical GDP Observation")
async def get_latest_gdp():
    cache_key = "gdp:latest"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    res = gdp_engine.get_latest_gdp()
    await set_cache(cache_key, res, ttl=1800)
    return res


@router.get("/forecast", response_model=ForecastResponse, summary="Generate Quarterly GDP Forecast")
async def forecast_gdp(
    quarters: int = Query(8, ge=1, le=24, description="Number of future quarters to forecast (1 to 24)"),
    model_type: str = Query("ARIMA-LSTM", description="Hybrid Model selection: ARIMA-LSTM, ARIMA-GRU, or ARIMA-CNN")
):
    if model_type not in ["ARIMA-LSTM", "ARIMA-GRU", "ARIMA-CNN"]:
        raise HTTPException(status_code=400, detail="Invalid model_type. Must be ARIMA-LSTM, ARIMA-GRU, or ARIMA-CNN.")

    cache_key = f"gdp:forecast:{model_type}:{quarters}"
    cached = await get_cache(cache_key)
    if cached:
        logger.info(f"Serving cached forecast for {model_type} ({quarters} quarters)")
        return cached

    latest = gdp_engine.get_latest_gdp()
    forecasts = gdp_engine.forecast_gdp(quarters=quarters, model_type=model_type)

    response_data = {
        "status": "success",
        "quarters_requested": quarters,
        "model_type": model_type,
        "latest_gdp": latest,
        "forecasts": forecasts
    }

    await set_cache(cache_key, response_data, ttl=3600)
    return response_data


@router.get("/models", summary="List Available Hybrid ML Architectures")
async def list_models():
    return {
        "available_models": [
            {
                "name": "ARIMA-LSTM",
                "description": "SOTA Hybrid model combining statistical ARIMA linear trend with 2-layer LSTM deep learning non-linear residual network.",
                "rmse": 133.7506,
                "mae": 51.3385,
                "r2": 0.9997,
                "rank": "🥇 Gold Winner"
            },
            {
                "name": "ARIMA-GRU",
                "description": "Fast-converging Hybrid model combining ARIMA with Gated Recurrent Unit neural network for residual estimation.",
                "rmse": 152.8332,
                "mae": 115.0697,
                "r2": 0.9996,
                "rank": "🥈 Silver Winner"
            },
            {
                "name": "ARIMA-CNN",
                "description": "Hybrid model using 1D Convolutional Neural Network for local temporal feature extraction on ARIMA residuals.",
                "rmse": 162.2732,
                "mae": 48.5734,
                "r2": 0.9996,
                "rank": "🥉 Best MAE"
            }
        ]
    }
