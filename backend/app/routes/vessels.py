from fastapi import APIRouter
from backend.app.services import nmpa_vessels as nmpa_v

router = APIRouter()

@router.get("/", summary="Get live vessel positions centered at New Mangalore Port (NMPA)")
def get_vessels():
    vessels = nmpa_v.get_nmpa_vessels()
    return {
        "port": "New Mangalore Port Authority (NMPA)",
        "vessels": vessels,
        "count": len(vessels)
    }

@router.get("/eta", summary="Get NMPA vessel ETA predictions")
def get_eta_predictions():
    vessels = nmpa_v.get_nmpa_vessels()
    eta_data = sorted(vessels, key=lambda v: v["hours_to_arrival"])
    return {"eta_predictions": eta_data}

@router.get("/congestion-alerts", summary="Get NMPA congestion alerts")
def get_congestion_alerts():
    alerts = nmpa_v.get_nmpa_congestion_alerts()
    return {"alerts": alerts, "count": len(alerts)}
