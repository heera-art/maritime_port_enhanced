"""
routing.py — FastAPI Router for New Mangalore Port Cargo Routing & Facility APIs
"""

from fastapi import APIRouter, Query, HTTPException, Body
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.app.services import routing as rservice

router = APIRouter(prefix="/routing", tags=["Cargo Routing & Facility Intelligence"])

class RoutingRequest(BaseModel):
    commodity: str = Field(default="TOTAL COAL", description="Commodity type to route")
    cargo_volume_tonnes: float = Field(default=50000.0, description="Monthly cargo tonnage")
    vessel_dwt: Optional[float] = Field(default=None, description="Vessel DWT (Deadweight Tonnage)")
    vessel_draft_m: Optional[float] = Field(default=None, description="Required vessel draught in meters")

@router.get("/facilities")
def get_nmpa_facilities() -> Dict[str, Any]:
    """Returns all 17 official New Mangalore Port Authority berths, draughts, and capacities."""
    facilities = rservice.get_all_facilities_list()
    return {
        "count": len(facilities),
        "port": "New Mangalore Port Authority (NMPA)",
        "facilities": facilities
    }

@router.post("/recommend")
def recommend_cargo_route(req: RoutingRequest) -> Dict[str, Any]:
    """
    Recommends NMPA berth facility and movement path based on commodity & vessel specifications.
    """
    return rservice.recommend_cargo_route(
        commodity=req.commodity,
        cargo_volume_tonnes=req.cargo_volume_tonnes,
        vessel_dwt=req.vessel_dwt,
        vessel_draft_m=req.vessel_draft_m
    )

@router.get("/integrated-pipeline")
def get_integrated_pipeline(
    commodity: str = Query(default="ALL", description="Commodity filter"),
    section: str = Query(default="ALL", description="Section filter (LOADED/UNLOADED/ALL)"),
    horizon: int = Query(default=6, description="Forecast horizon in months")
) -> Dict[str, Any]:
    """
    INTEGRATED PIPELINE ENDPOINT:
    Connects Cargo Forecast -> Capacity Analysis -> Facility Routing Recommendation.
    """
    return rservice.get_integrated_forecast_routing(
        commodity=commodity,
        section=section,
        horizon=horizon
    )
