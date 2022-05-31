import requests


def get_tomorrow_weather(lat, lon):
    API_KEY = '<tomorrow.io API KEY>'
    params = {'units': 'metric', 'timesteps': '1d', 'apikey': API_KEY,
              'location': str(lat) + ',' + str(
                  lon), 'fields': 'temperature,humidity,windSpeed,weatherCodeFullDay'}
    url = 'https://api.tomorrow.io/v4/timelines?'

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip"
    }

    return requests.get(url, params=params, headers=headers)
