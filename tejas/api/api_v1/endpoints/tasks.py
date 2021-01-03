from fastapi import APIRouter

from tejas.core.boto_client import tasks_table

router = APIRouter()


@router.get("/task_details")
def task_details(*, task_id: str):
    task_return = tasks_table.get_item(
        Key={
            "taskId": task_id
        }
    )['Item']

    return task_return

