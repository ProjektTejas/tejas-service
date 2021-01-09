import json
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from pathlib import Path

from tejas import schemas, settings
from tejas.core.boto_client import lambda_client, tasks_table

router = APIRouter()


@router.post("/train_model", response_model=schemas.TaskId)
def create_train_task(
    *, model_name: str = Form(...), file: UploadFile = File(...)
):

    dataset_path = settings.DATASETS_PATH / file.filename

    # reset the file cursor
    file.file.seek(0)
    save_upload_file(file, dataset_path)

    # invoke the model training process
    task_id: str = str(uuid.uuid4())
    lambda_client.invoke(
        FunctionName=settings.TEJAS_MODEL_TRAIN_LAMBDA_ARN,
        InvocationType="Event",
        Payload=json.dumps({
            "taskId": task_id,
            "args": {
                "datasetZip": str(dataset_path),
                "modelName": model_name
            }
        }),
    )

    return {"taskId": task_id}


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


@router.get("/download_model")
def download_model(*, task_id: str):
    task_return = tasks_table.get_item(
        Key={
            "taskId": task_id
        }
    )['Item']

    model_path = task_return['taskResult']['modelPath']

    return FileResponse(model_path)
