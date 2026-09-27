from app.core.http_client import http_client
from app.core.config import settings


class WeatherClient:
    BASE_URL = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    async def get_weather(self, city: str):

        params = {
            "q": city,
            "appid": settings.weather_api_key,
            "units": "metric",
            "lang": "ru"
        }

        async with http_client.session.get(
            self.BASE_URL,
            params=params
        ) as response:

            response.raise_for_status()

            return await response.json()