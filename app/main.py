from fastapi import FastAPI
import aiohttp

from app.api.health import router as health_router
from app.api.weather import router as weather_router
from app.api.github import router as github_router
from app.api.tasks import router as tasks_router

from app.core.http_client import http_client

app = FastAPI(
    title="AI Assistant Platform",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    http_client.session = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown():
    await http_client.session.close()


app.include_router(health_router)
app.include_router(weather_router)
app.include_router(github_router)
app.include_router(tasks_router)