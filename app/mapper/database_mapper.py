from app.model.weather_db import WeatherDB
from app.model.weather_do import WeatherDO


class DBmapper:

    @staticmethod
    def domain_to_db(weather: WeatherDO) -> WeatherDB:
        return WeatherDB(date=weather.startTime, humidity=weather.humidity, temperature=weather.temperature, sunrisetime=weather.sunriseTime, sunsettime=weather.sunsetTime, windspeed=weather.windSpeed)