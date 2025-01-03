# filepath: /c:/Users/Asus/Desktop/Varonis/restaurant-manager-api/app/api.py
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/query")
async def get_query_param(param: str):
    return {"received_param": param}

@router.get("/header")
async def get_header_param(request: Request):
    header_param = request.headers.get('X-String-Param')
    return {"received_header": header_param}