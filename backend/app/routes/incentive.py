from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services import synthetic_data as sd

router = APIRouter()

class MonteCarloRequest(BaseModel):
    scenario: str = "container_charge"
    charge_delta: float = -5.0
    incentive_pct: float = 8.0

@router.get("/recommendations")
def get_recommendations():
    return {"recommendations": sd.generate_incentive_recommendations()}

@router.post("/monte-carlo")
def run_monte_carlo(req: MonteCarloRequest):
    return sd.run_monte_carlo(req.scenario, req.charge_delta, req.incentive_pct)
