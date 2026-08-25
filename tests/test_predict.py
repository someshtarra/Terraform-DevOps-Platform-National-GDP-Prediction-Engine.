import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_latest_gdp(async_client: AsyncClient):
    response = await async_client.get("/api/v1/latest")
    assert response.status_code == 200
    data = response.json()
    assert "gdp" in data
    assert "date" in data


@pytest.mark.asyncio
async def test_forecast_gdp_valid(async_client: AsyncClient):
    response = await async_client.get("/api/v1/forecast?quarters=4&model_type=ARIMA-LSTM")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["forecasts"]) == 4
    assert data["model_type"] == "ARIMA-LSTM"


@pytest.mark.asyncio
async def test_forecast_gdp_invalid_model(async_client: AsyncClient):
    response = await async_client.get("/api/v1/forecast?quarters=4&model_type=INVALID_MODEL")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_list_models(async_client: AsyncClient):
    response = await async_client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert len(data["available_models"]) == 3
