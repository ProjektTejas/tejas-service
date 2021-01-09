import json
import uuid

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from loguru import logger

from tejas.api.api_v1.api import api_router
from tejas.api.api_v1.exceptions import TrainingNotCompleted
from tejas.core.config import settings
from tejas.core.boto_client import lambda_client

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

if settings.ALLOW_ALL_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(TrainingNotCompleted)
async def training_not_completed_exception_handler(
    request: Request, exc: TrainingNotCompleted
):
    return JSONResponse(
        status_code=412,
        content={
            "error": TrainingNotCompleted.__name__,
            "message": f"Training Not Completed for : {exc.task_id}",
        },
    )


@app.get("/")
def read_root():
    return {"hello", "world"}


@app.get("/invoke")
async def invoke_train():
    logger.info(f"Invoking: {settings.TEJAS_MODEL_TRAIN_LAMBDA_ARN}")

    lambda_client.invoke(
        FunctionName=settings.TEJAS_MODEL_TRAIN_LAMBDA_ARN,
        InvocationType="Event",
        Payload=json.dumps(
            {
                "taskId": str(uuid.uuid4()),
                "args": {
                    "datasetZip": str(
                        settings.DATASETS_PATH / "indian-face-dataset.zip"
                    ),
                    "modelName": "mobilenet_v2",
                },
            }
        ),
    )

    return {"invoked": "successfully"}


# web sockets do not work with mangum, so we will have to halt this for now
# @app.websocket("/")
# async def websock_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was : {data}")
