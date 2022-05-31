from sqlalchemy import Column, Integer, DateTime, String
from app.database.database import Base


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTime)
    place = Column(String, unique=False)
    temperature = Column(String, unique=False)
    humidity = Column(String, unique=False)
    windspeed = Column(String)
