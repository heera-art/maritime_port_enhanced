from fastapi import APIRouter, Query
from backend.app.services import synthetic_data as sd

router = APIRouter()

@router.get("/scenarios")
def get_scenarios():
    return {"scenarios": list(sd.DIGITAL_TWIN_SCENARIOS.keys()),
            "details": sd.DIGITAL_TWIN_SCENARIOS}

@router.get("/scenario/{scenario_key}")
def get_scenario(scenario_key: str):
    result = sd.get_twin_scenario(scenario_key)
    if not result:
        return {"error": f"Unknown scenario '{scenario_key}'"}
    return {"scenario_key": scenario_key, "result": result,
            "monte_carlo": sd.get_twin_monte_carlo(scenario_key)}

@router.get("/berths")
def get_berth_map():
    return {"berths": sd.generate_berth_status(12)}
