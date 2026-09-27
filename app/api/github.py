from fastapi import APIRouter

from app.services.github_service import GitHubService

router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)

service = GitHubService()


@router.get("/{username}")
async def get_user(username: str):
    return await service.get_user(username)


@router.get("/full/{username}")
async def get_full_profile(username: str):
    return await service.get_full_profile(username)


@router.get("/stats/{username}")
async def get_stats(username: str):
    return await service.get_stats(username)