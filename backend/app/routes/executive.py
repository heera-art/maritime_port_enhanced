from fastapi import APIRouter
from backend.app.services import synthetic_data as sd

router = APIRouter()

@router.get("/kpis")
def get_kpis():
    return sd.generate_kpis()

@router.get("/events")
def get_port_events():
    return {"events": sd.generate_port_events()}

@router.get("/revenue-trend")
def get_revenue_trend():
    return sd.generate_revenue_trend(30)
