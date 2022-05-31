from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from geopy.geocoders import Nominatim
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.api.tomorrow_weather import get_tomorrow_weather
from app.database import crud, models
from app.database.database import engine, SessionLocal
from app.mapper.mapper_code import weather_mapper
from app.model.weather_do import WeatherDO
from app.model.weather_forecast_do import WeatherForecastDO
router = APIRouter()
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/weather")
async def read_root():
    return {"Hello": "World"}


# API to get weather updates for the current date

@router.get("/weather/daily/{city}")
async def get_weather_daily(city: str, db: Session = Depends(get_db)):

    geolocator = Nominatim(user_agent="Test1")
    location = geolocator.geocode(city.strip())

    if location is None:
        return Response("Bad Request", status_code=400)

    # calling external api tomorrow.io
    response = get_tomorrow_weather(location.latitude, location.longitude)
    output = response.json()
    weatherdict = {"place": city.upper(), "forecastdate": output["data"]["timelines"][0]["intervals"][0]["startTime"],
                   "humidity": output["data"]["timelines"][0]["intervals"][1]["values"]["humidity"],
                   "temperature": output["data"]["timelines"][0]["intervals"][1]["values"]["temperature"],
                   "windSpeed": output["data"]["timelines"][0]["intervals"][1]["values"]["windSpeed"],
                   "weatherCodeFullDay": output["data"]["timelines"][0]["intervals"][1]["values"]["weatherCodeFullDay"]}
    # check if the data already exist else create a new entry
    forecastdata = crud.get_current_weather_data(db, weatherdict["forecastdate"], city.upper())
    if len(forecastdata) == 0:
        crud.create_current_weather_data(db, weatherdict)

    weather_code = str(weatherdict["weatherCodeFullDay"])
    weatherdict["Description"] = weather_mapper(weather_code)
    response_json = pydantic_model(weatherdict)

    return response_json


def pydantic_model(weatherdict) -> WeatherDO:
    return WeatherDO(date=weatherdict["forecastdate"], description=weatherdict["Description"],
                     city=weatherdict["place"], temperature=weatherdict["temperature"],
                     humidity=weatherdict["humidity"], windSpeed=weatherdict["windSpeed"],
                     weatherCode=weatherdict["weatherCodeFullDay"])


def pydantic_model2(weatherdict) -> WeatherForecastDO:
    return WeatherForecastDO(date=weatherdict["forecastdate"], description=weatherdict["Description"],
                             temperature=weatherdict["temperature"], weatherCode=weatherdict["weatherCodeFullDay"])


# API to get weather forecast for next 10 days

@router.get("/weather/forecast/{city}")
async def get_weather_forecast(city: str, db: Session = Depends(get_db)):
    geolocator = Nominatim(user_agent="Test1")
    location = geolocator.geocode(city.strip())

    if location is None:
        return Response("Bad Request", status_code=400)
    # calling external api tomorrow.io
    response = get_tomorrow_weather(location.latitude, location.longitude)
    output = response.json()
    weather_history = []
    history_data = output["data"]["timelines"][0]["intervals"]
    history_data = history_data[:10]
    for i in history_data:
        weather = {}
        weather["forecastdate"] = i["startTime"]
        weather["temperature"] = i["values"]["temperature"]
        weather["weatherCodeFullDay"] = str(i["values"]["weatherCodeFullDay"])
        weather["Description"] = weather_mapper(weather["weatherCodeFullDay"])
        weather_history.append(pydantic_model2(weather))

    return weather_history


#  API to compare current weather with past 3 days

@router.get("/weather/comparison/{city}")
async def get_weather_history(city: str, db: Session = Depends(get_db)):
    two_day = timedelta(hours=48)
    weather_history = crud.get_weather_history(db, datetime.now() - two_day, city.upper())
    if len(weather_history) != 0 and len(weather_history) != 1:
        today_temp = weather_history[-1].temperature
        previous_temp = weather_history[-2].temperature

        if float(today_temp) > float(previous_temp):
            return "warmer"
        else:
            return "colder"
