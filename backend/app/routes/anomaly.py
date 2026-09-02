from fastapi import APIRouter, Query
from backend.app.services import synthetic_data as sd

router = APIRouter()

@router.get("/events")
def get_anomaly_events():
    return {"events": sd.generate_anomaly_events()}

@router.get("/history")
def get_anomaly_history(days: int = Query(default=30, ge=7, le=90)):
    return {"history": sd.generate_anomaly_history(days)}
