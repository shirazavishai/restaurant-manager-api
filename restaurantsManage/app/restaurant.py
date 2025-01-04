from datetime import datetime
import json
from pydantic import BaseModel

class Restaurant(BaseModel):
    name: str
    style: str
    address: str
    open_hour: str
    close_hour: str
    vegetarian: str
    delivery: str


    def to_string(self):
        return f"{{\"name\": \"{self.name}\", \"style\": \"{self.style}\", \"address\": \"{self.address}\", \"openHour\": \"{self.open_hour}\", \"closeHour\": \"{self.close_hour}\", \"vegetarian\": \"{self.vegetarian}\", \"delivers\": \"{self.delivery}\"}}"
    
    def to_json_string(self):
        return json.dumps(self.__dict__)

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
