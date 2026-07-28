import requests

from langchain_core.tools import tool

from config.settings import OPENWEATHER_API_KEY


@tool
def get_weather(city: str):
    """
    Get the current weather of any city.
    Use this tool whenever the user asks about weather,
    temperature, humidity, rain, climate, or forecast.
    """

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }