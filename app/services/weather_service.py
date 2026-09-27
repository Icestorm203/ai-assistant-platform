import json

from app.cache.redis_client import redis_client
from app.clients.weather_client import WeatherClient
from app.schemas.weather import WeatherResponse

class WeatherService:
    def __init__(self):
        self.client = WeatherClient()

    async def get_weather(
        self,
        city: str
    ) -> WeatherResponse:

        cache_key = f"weather:{city}"

        cached_data = await redis_client.get(cache_key)

        if cached_data:

            print("CACHE HIT")

            data = json.loads(cached_data)

            return WeatherResponse(**data)

        print("CACHE MISS")

        weather_data = await self.client.get_weather(city)

        result = {
            "city": weather_data["name"],
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "description": weather_data["weather"][0]["description"]
        }

        await redis_client.set(
            cache_key,
            json.dumps(result),
            ex=60
        )

        return WeatherResponse(**result)