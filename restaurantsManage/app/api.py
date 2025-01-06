# filepath: /c:/Users/Asus/Desktop/Varonis/restaurant-manager-api/app/api.py
import json
from fastapi import APIRouter
import app.service as service
import app.logger as logger

router = APIRouter()


@router.get("/find_restaurant")
async def get_query_param(sentence: str = "An italian restaurant that opens at 08:00 vegi"):
    logger.logger.info(f"{__name__}: Received query: {sentence}")
    return {service.search_required_restaurant(sentence)  }

@router.get("/all_restaurants")
async def get_all_restaurants():
    logger.logger.info(f"{__name__}: Received request for all restaurants")
    if(service.restaurants == []):
        return {"No restaurants found"}
    return {json.dumps(service.restaurants)}

