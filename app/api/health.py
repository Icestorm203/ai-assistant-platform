from fastapi import APIRouter
from app.cache.redis_client import redis_client

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {
        "status": "ok"
    }


@router.get("/cache/{key}")
async def get_cache_value(key: str):

    value = await redis_client.get(key)

    return {
        "key": key,
        "value": value
    }