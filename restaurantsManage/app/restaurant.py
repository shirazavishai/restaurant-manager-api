from datetime import datetime
from pydantic import BaseModel

class Restaurant(BaseModel):
    name: str
    style: str
    address: str
    open_hour: str
    close_hour: str
    vegetarian: bool
    delivery: bool

# Check if the restaurant is open based on the current time
def is_open_now(open_hour, close_hour):
    now = datetime.now().time()
    open_time = datetime.strptime(open_hour, '%H:%M').time()
    close_time = datetime.strptime(close_hour, '%H:%M').time()

    return open_time <= now <= close_time

def is_open_at_time(requested_time, open_hour, close_hour):
    requested_time = datetime.strptime(requested_time, '%H:%M').time()
    open_time = datetime.strptime(open_hour, '%H:%M').time()
    close_time = datetime.strptime(close_hour, '%H:%M').time()

    return open_time <= requested_time <= close_time