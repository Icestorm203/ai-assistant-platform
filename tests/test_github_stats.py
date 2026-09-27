from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.services.github_service.redis_client.set", new_callable=AsyncMock)
@patch("app.services.github_service.redis_client.get", new_callable=AsyncMock)
@patch("app.services.github_service.GitHubClient.get_repos")
def test_github_stats_endpoint(
    mock_repos,
    mock_get,
    mock_set
):
    mock_get.return_value = None

    mock_repos.return_value = [
        {
            "language": "Python"
        },
        {
            "language": "Python"
        },
        {
            "language": "C++"
        }
    ]

    response = client.get(
        "/github/stats/Icestorm203"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_repositories"] == 3
    assert data["languages"]["Python"] == 2