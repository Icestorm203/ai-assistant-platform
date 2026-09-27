from pydantic import BaseModel


class GitHubUserResponse(BaseModel):
    login: str
    public_repos: int
    followers: int
    following: int


class GitHubRepoResponse(BaseModel):
    name: str
    language: str | None
    stargazers_count: int


class GitHubFullResponse(BaseModel):
    login: str
    public_repos: int
    followers: int
    following: int
    repos: list[GitHubRepoResponse]


class GitHubStatsResponse(BaseModel):
    total_repositories: int
    languages: dict[str, int]
