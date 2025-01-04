# filepath: /c:/Users/Asus/Desktop/Varonis/restaurant-manager-api/app/api.py
from fastapi import APIRouter, Request
import app.service as service

router = APIRouter()


# A mock restaurant list
restaurants_db = [
    {"name": "Pizza Hut", "style": "Italian", "address": "Wherever street 99, Somewhere", "openHour": "09:00", "closeHour": "23:00", "vegetarian": "yes", "delivers": "yes"},
    {"name": "Le Bistrot", "style": "French", "address": "Paris Road 12, Paris", "openHour": "10:00", "closeHour": "22:00", "vegetarian": "no", "delivers": "no"},
    {"name": "Green Bowl", "style": "Italian", "address": "Veggie Street 15, Healthy City", "openHour": "08:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"}
]


@router.get("/find_restaurant")
async def get_query_param(param: str):
    return {service.search_required_restaurant(param)  }

@router.get("/header")
async def get_header_param(request: Request):
    header_param = request.headers.get('X-String-Param')
    return {"received_header": header_param}

@router.get("/find_restaurant2")
async def get_query_param2(style: str, vegetarian: str, current_time: str, request: Request):
    service.search_required_restaurant(param)    
    return {"received_param": param}
