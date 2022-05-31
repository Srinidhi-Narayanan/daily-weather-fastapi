from pydantic import BaseModel
from datetime import datetime


class WeatherForecastDO(BaseModel):
    date: datetime
    temperature: str
    description: str
    weatherCode: str

