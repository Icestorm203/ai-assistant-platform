from app.core.http_client import http_client


class GitHubClient:
    BASE_URL = "https://api.github.com/users"

    async def get_user(self, username: str) -> dict:

        async with http_client.session.get(
            f"{self.BASE_URL}/{username}"
        ) as response:

            response.raise_for_status()

            return await response.json()

    async def get_repos(self, username: str) -> list:

        async with http_client.session.get(
            f"{self.BASE_URL}/{username}/repos"
        ) as response:

            response.raise_for_status()

            return await response.json()