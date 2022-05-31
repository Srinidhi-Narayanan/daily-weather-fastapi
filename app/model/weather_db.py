from pydantic import BaseModel
from datetime import datetime


class WeatherDB(BaseModel):
    date: datetime
    place: str
    temperature: str
    humidity: str
    windspeed: str
