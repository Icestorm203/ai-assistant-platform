from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.weather import router as weather_router
from app.api.github import router as github_router
from app.api.tasks import router as tasks_router

from app.core.http_client import http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    http_client.session = aiohttp.ClientSession()

    yield

    # --- shutdown ---
    await http_client.session.close()


app = FastAPI(
    title="AI Assistant Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(weather_router)
app.include_router(github_router)
app.include_router(tasks_router)