# filepath: /c:/Users/Asus/Desktop/Varonis/restaurant-manager-api/app/api.py
import json
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
async def get_query_param(sentence: str = "An italian restaurant that opens at 08:00 vegi"):
    return {service.search_required_restaurant(sentence)  }

@router.get("/all_restaurants")
async def get_all_restaurants():
    return {json.dumps(service.restaurants)}

