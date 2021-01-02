from celery.result import AsyncResult
from fastapi import APIRouter

from tejas.core.celery_app import celery_app

router = APIRouter()


@router.get("check_task/{id}")
def check_task(task_id: str):
    task: AsyncResult = celery_app.AsyncResult(task_id)
