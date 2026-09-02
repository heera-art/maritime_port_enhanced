from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services import synthetic_data as sd

router = APIRouter()

class QueryRequest(BaseModel):
    query: str = ""
    context: dict = {}

@router.post("/query")
def process_query(req: QueryRequest):
    trace = sd.generate_agent_trace(req.query)
    response = sd.generate_copilot_response(req.query)
    return {"trace": trace, "response": response}

@router.get("/suggested-queries")
def get_suggested_queries():
    return {"queries": sd.SUGGESTED_QUERIES}
