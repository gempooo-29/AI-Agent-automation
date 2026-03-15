import requests
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a specific city.
    Use this when the user asks about the weather in any location.

    Args:
        city: The name of the city (e.g. 'Cairo', 'London')

    Returns:
        Current weather information for the city.
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()

        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        wind_speed = current["windspeedKmph"]
        description = current["weatherDesc"][0]["value"]

        return (
            f"Weather in {city}:\n"
            f"- Status: {description}\n"
            f"- Temperature: {temp_c}°C (feels like {feels_like}°C)\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind Speed: {wind_speed} km/h"
        )

    except Exception as e:
        return f"Could not get weather for '{city}': {str(e)}"