import requests

from config import OPENWEATHER_API_KEY


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    """
    Fetch current weather for a given city.

    Returns:
        {
            "city": "Goa",
            "temperature": 30.5,
            "feels_like": 34.1,
            "humidity": 78,
            "condition": "Clouds",
            "description": "broken clouds",
            "wind_speed": 5.4
        }

    Raises:
        Exception if the API request fails.
    """

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"Weather API Error: {response.text}")

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }