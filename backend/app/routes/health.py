from fastapi import APIRouter
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "YellowSense Maritime Intelligence API v2.0"}
