from fastapi import APIRouter

from app.services.weather_service import WeatherService
from aiohttp import ClientResponseError

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)

service = WeatherService()


@router.get("/{city}")
async def get_weather(city: str):
    try:
        return await service.get_weather(city)

    except ClientResponseError as e:
        raise HTTPException(
            status_code=e.status,
            detail=e.message
        )


