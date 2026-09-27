import asyncio
import json

from app.clients.github_client import GitHubClient
from app.schemas.github import (
    GitHubUserResponse,
    GitHubRepoResponse,
    GitHubFullResponse,
    GitHubStatsResponse
)
from collections import Counter
from app.cache.redis_client import redis_client

class GitHubService:
    def __init__(self):
        self.client = GitHubClient()

    async def get_user(self, username: str) -> GitHubUserResponse:
        data = await self.client.get_user(username)

        return GitHubUserResponse(
            login=data["login"],
            public_repos=data["public_repos"],
            followers=data["followers"],
            following=data["following"]
        )

    async def get_full_profile(
        self,
        username: str
    ) -> GitHubFullResponse:

        user_data, repos_data = await asyncio.gather(
            self.client.get_user(username),
            self.client.get_repos(username)
        )

        repos = [
            GitHubRepoResponse(
                name=repo["name"],
                language=repo["language"],
                stargazers_count=repo["stargazers_count"]
            )
            for repo in repos_data
        ]

        return GitHubFullResponse(
            login=user_data["login"],
            public_repos=user_data["public_repos"],
            followers=user_data["followers"],
            following=user_data["following"],
            repos=repos
        )
    

    async def get_stats(
        self,
        username: str
    ) -> GitHubStatsResponse:

        cache_key = f"github_stats:{username}"

        cached_data = await redis_client.get(
            cache_key
        )

        if cached_data:

            print("CACHE HIT")

            return GitHubStatsResponse(
                **json.loads(cached_data)
            )

        print("CACHE MISS")

        repos = await self.client.get_repos(
            username
        )

        languages = Counter()

        for repo in repos:

            language = repo["language"]

            if language:
                languages[language] += 1

        result = {
            "total_repositories": len(repos),
            "languages": dict(languages)
        }

        await redis_client.set(
            cache_key,
            json.dumps(result),
            ex=60
        )

        return GitHubStatsResponse(
            **result
        )