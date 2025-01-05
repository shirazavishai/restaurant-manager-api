# filepath: /c:/Users/Asus/Desktop/Varonis/restaurant-manager-api/main.py
from fastapi import FastAPI
from app.api import router
import app.logger as logger

app = FastAPI()

app.include_router(router)

logger.logger.info(__name__+": Starting the application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)