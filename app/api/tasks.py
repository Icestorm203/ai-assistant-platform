from fastapi import APIRouter

from app.tasks.celery_app import celery_app
from celery.result import AsyncResult
from app.tasks.report_tasks import generate_github_report

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/github-report/{username}")
async def github_report(username: str):

    task = generate_github_report.delay(
        username
    )

    return {
        "task_id": task.id
    }


@router.get("/{task_id}")
async def get_task_status(task_id: str):

    task = AsyncResult(
        task_id,
        app=celery_app
    )

    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result
    }