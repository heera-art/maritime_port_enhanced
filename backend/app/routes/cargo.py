from fastapi import APIRouter, Query, Body
from typing import Optional
from backend.app.services import forecasting as fservice
from backend.app.services import synthetic_data as sd

router = APIRouter()

@router.get("/forecast", summary="Get data-grounded ML cargo volume forecast")
def get_forecast(
    horizon: int = Query(default=6, ge=1, le=24, description="Horizon in months"),
    commodity: str = Query(default="ALL", description="Filter commodity"),
    section: str = Query(default="ALL", description="Filter flow section (LOADED / UNLOADED)")
):
    return fservice.get_enhanced_cargo_forecast(
        horizon_months=horizon,
        commodity=commodity,
        section=section
    )

@router.get("/commodities", summary="List unique commodities and flow sections in dataset")
def get_commodities():
    return fservice.get_available_commodities()

@router.get("/accuracy", summary="Chronological backtesting: Baseline vs Primary ML Model")
def get_accuracy(
    commodity: str = Query(default="ALL"),
    section: str = Query(default="ALL")
):
    return fservice.evaluate_forecast_models(commodity=commodity, section=section)

@router.get("/explainability", summary="Forecast drivers and influencing factor weights")
def get_explainability(
    commodity: str = Query(default="ALL"),
    section: str = Query(default="ALL")
):
    res = fservice.get_enhanced_cargo_forecast(horizon_months=6, commodity=commodity, section=section)
    return {
        "commodity": commodity,
        "section": section,
        "drivers": res.get("drivers", []),
        "trend_signal": res.get("summary", {}).get("trend_signal"),
    }

@router.get("/data-quality", summary="Data completeness, missing values, and lineage metrics")
def get_data_quality():
    return fservice.get_data_quality_report()

@router.post("/scenario", summary="Run interactive What-If cargo scenario simulation")
def run_scenario(payload: dict = Body(...)):
    commodity = payload.get("commodity", "ALL")
    section = payload.get("section", "ALL")
    vessel_change = float(payload.get("vessel_arrival_change_pct", 0.0))
    demand_change = float(payload.get("trade_demand_change_pct", 0.0))
    weather_delay = float(payload.get("weather_delay_days", 0.0))
    horizon = int(payload.get("horizon_months", 6))

    return fservice.simulate_cargo_scenario(
        commodity=commodity,
        section=section,
        vessel_arrival_change_pct=vessel_change,
        trade_demand_change_pct=demand_change,
        weather_delay_days=weather_delay,
        horizon_months=horizon
    )

@router.get("/berths", summary="Berth occupancy status")
def get_berths():
    return {"berths": sd.generate_berth_status(12)}
