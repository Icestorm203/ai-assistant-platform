from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.services.weather_service.redis_client.set", new_callable=AsyncMock)
@patch("app.services.weather_service.redis_client.get", new_callable=AsyncMock)
@patch("app.services.weather_service.WeatherClient.get_weather")
def test_weather_endpoint(
    mock_weather,
    mock_get,
    mock_set
):
    mock_get.return_value = None

    mock_weather.return_value = {
        "name": "Moscow",
        "main": {
            "temp": 20,
            "humidity": 50
        },
        "weather": [
            {
                "description": "clear sky"
            }
        ]
    }

    response = client.get("/weather/Moscow")

    assert response.status_code == 200