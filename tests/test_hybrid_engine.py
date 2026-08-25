from app.models.hybrid_engine import GDPHybridEngine


def test_hybrid_engine_initialization():
    engine = GDPHybridEngine()
    assert engine.is_loaded is True
    assert engine.df is not None


def test_hybrid_engine_forecast():
    engine = GDPHybridEngine()
    forecasts = engine.forecast_gdp(quarters=8, model_type="ARIMA-LSTM")
    assert len(forecasts) == 8
    assert forecasts[0]["forecast_gdp_billions"] > 0
    assert forecasts[0]["upper_bound_billions"] >= forecasts[0]["forecast_gdp_billions"]
    assert forecasts[0]["lower_bound_billions"] <= forecasts[0]["forecast_gdp_billions"]
