from fastapi import APIRouter
from backend.app.services import synthetic_data as sd

router = APIRouter()

@router.get("/status")
def get_pipeline_status():
    return sd.generate_pipeline_metrics()

@router.get("/log")
def get_pipeline_log():
    return {"events": sd.generate_pipeline_log()}
