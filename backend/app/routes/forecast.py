"""
Forecast Routes — AI Intelligence API
---------------------------------------
Exposes the four forecasting engines as REST endpoints.
All responses are JSON-serialisable dicts returned directly
from the service layer — no ORM, no DB, no heavy deps.

Endpoints:
  GET /forecast/cargo           — 7-day cargo volume forecast
  GET /forecast/congestion      — congestion risk + 24h prediction
  GET /forecast/trade           — import/export trend analysis
  GET /forecast/recommendations — prioritised operational advisories
"""

from fastapi import APIRouter
from backend.app.services.forecasting import (
    forecast_cargo,
    forecast_congestion,
    forecast_trade,
    generate_recommendations,
)

router = APIRouter(prefix="/forecast", tags=["Forecasting & Intelligence"])


@router.get("/cargo", summary="7-day cargo volume forecast with confidence score")
def cargo_forecast():
    return forecast_cargo()


@router.get("/congestion", summary="Port congestion risk score and 24h prediction")
def congestion_forecast():
    return forecast_congestion()


@router.get("/trade", summary="Import/export trend analysis with 3-month projection")
def trade_forecast():
    return forecast_trade()


@router.get("/recommendations", summary="AI-generated operational recommendations")
def recommendations():
    return generate_recommendations()
