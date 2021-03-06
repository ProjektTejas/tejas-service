import json
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
from zipfile import ZipFile
from loguru import logger
from datetime import datetime

from tejas import schemas, settings
from tejas.core.boto_client import (
    tasks_table,
    s3_client,
    download_models_bucket,
)

router = APIRouter()


@router.post("/train_model", response_model=schemas.TaskId)
def create_train_task(*, model_name: str = Form(...), file: UploadFile = File(...)):

    # now deprecated
    # dataset_path = settings.DATASETS_PATH / file.filename

    # reset the file cursor
    file.file.seek(0)
    # save the file in tmp folder
    temp_file_path = Path("/tmp") / file.filename
    save_upload_file(file, temp_file_path)

    # upload it to S3 bucket
    datasets_bucket = settings.DATASETS_BUCKET

    # invoke the model training process

    # create the task in DDB
    task_id: str = str(uuid.uuid4())
    task_args = {
        "taskId": task_id,
        "args": {
            "modelName": model_name,
            "dataset": file.filename,
            "bucket": settings.DATASETS_BUCKET,
        },
    }

    logger.info(f"Creating Task: {task_args}")

    # instantiate the task in db
    new_task = {
        "taskId": task_id,
        "taskArgs": task_args,
        "taskStatus": "INITIALIZING",
        "taskResult": "",
        "timestamp": datetime.now().isoformat(),
    }
    tasks_table.put_item(Item=new_task)

    # upload to S3 which triggers training
    s3_client.upload_file(
        str(temp_file_path),
        datasets_bucket,
        file.filename,
        ExtraArgs={"Metadata": {"args": json.dumps(task_args)}},
    )

    # deprecated
    # # invoke the model training process
    # task_id: str = str(uuid.uuid4())
    # lambda_client.invoke(
    #     FunctionName=settings.TEJAS_MODEL_TRAIN_LAMBDA_ARN,
    #     InvocationType="Event",
    #     Payload=json.dumps(
    #         {
    #             "taskId": task_id,
    #             "args": {"datasetZip": str(dataset_path), "modelName": model_name},
    #         }
    #     ),
    # )

    return {"taskId": task_id}


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


@router.get("/download_model")
def download_model(*, task_id: str):
    task_return = tasks_table.get_item(Key={"taskId": task_id})["Item"]

    model_path = task_return["taskResult"]["modelPath"]
    idx_to_classname_path = task_return["taskResult"]["idxToClassnamePath"]

    # this does not work
    # return FileResponse(model_path)

    # this does not work, we have a 6 MB cap limit for the payload size
    # i.e. directly returning this file as a response
    model_zip_path = f"{str(settings.MODELS_PATH / task_return['taskId'])}.zip"

    # check if the object exists in s3
    objs = list(download_models_bucket.objects.filter(Prefix=Path(model_zip_path).name))
    if len(objs) == 0:
        # file does not exist, create it
        with ZipFile(model_zip_path, "w") as zipf:
            zipf.write(model_path, Path(model_path).name)
            zipf.write(idx_to_classname_path, Path(idx_to_classname_path).name)

        # upload this zip file to S3
        download_models_bucket.upload_file(model_zip_path, Path(model_zip_path).name)

    # get a pre-signed url
    response = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.MODELS_BUCKET, "Key": Path(model_zip_path).name},
        ExpiresIn=300,
    )  # expires in 5 mins

    logger.info(f"PreSigned Download URL: {response}")

    return {"download_url": response}
