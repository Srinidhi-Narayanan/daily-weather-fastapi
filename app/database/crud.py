from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models


def get_current_weather_data(db: Session, date: datetime, city: str):
    return db.query(models.Weather).filter(and_(models.Weather.date == date, models.Weather.place == city)).all()


def create_current_weather_data(db: Session, weather):
    db_data = models.Weather(date=weather["forecastdate"], place=weather["place"], humidity=weather["humidity"],
                             temperature=weather["temperature"], windspeed=weather["windSpeed"])
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_weather_history(db: Session, date: datetime, city: str):
    return db.query(models.Weather).filter(and_(models.Weather.date >= date, models.Weather.place == city)).all()
