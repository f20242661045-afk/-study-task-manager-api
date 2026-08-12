import httpx


WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }

    try:
        response = httpx.get(
            WEATHER_API_URL,
            params=params,
            timeout=10.0,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "timezone": data["timezone"],
            "current": data["current"],
        }

    except httpx.HTTPError as error:
        raise RuntimeError(
            "Weather service request failed."
        ) from error