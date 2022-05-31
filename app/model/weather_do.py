from pydantic import BaseModel
from datetime import datetime


class WeatherDO(BaseModel):
    date: datetime
    description: str
    city:str
    temperature: str
    humidity: str
    windSpeed: str
    weatherCode: str
