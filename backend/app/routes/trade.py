from fastapi import APIRouter
from backend.app.services import synthetic_data as sd

router = APIRouter()

@router.get("/lanes")
def get_trade_lanes():
    return {"lanes": sd.generate_trade_lanes()}

@router.get("/commodity-prices")
def get_commodity_prices():
    return {"prices": sd.generate_commodity_prices()}

@router.get("/opportunities")
def get_market_opportunities():
    return {"opportunities": sd.generate_market_opportunities()}
