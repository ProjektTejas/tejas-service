import json
from io import BytesIO
from typing import Dict, Any

import torch
import torchvision.transforms as T
import torch.nn.functional as F

from PIL import Image
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from torch import Tensor
from torch.jit import ScriptModule

from loguru import logger

from tejas import schemas
from tejas.api.api_v1.exceptions import TrainingNotCompleted
from tejas.core.boto_client import tasks_table

router = APIRouter()


@router.post("/classify_image")
async def classify_image(*, task_id: str = Form(...), file: UploadFile = File(...)):

    # fetch the model details of task
    task = tasks_table.get_item(Key={"taskId": task_id})["Item"]

    logger.info(f"Received classify for {task}")

    if task["taskStatus"] != "COMPLETED":
        raise TrainingNotCompleted(task_id=task_id)

    # load the model
    model: ScriptModule = torch.jit.load(task["taskResult"]["modelPath"])

    # load the idxToClass
    with open(task["taskResult"]["idxToClassnamePath"], "r") as f:
        idx_to_classname: Dict[str, str] = json.load(f)

    # create the transforms based on the model type
    if task["taskArgs"]["modelName"] == "mobilenet_v2":
        transform: T.Compose = T.Compose(
            [
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
    else:
        transform: T.Compose = T.Compose(
            [
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

    # reset the file cursor
    file.file.seek(0)
    contents = await file.read()
    # load the image file
    image = Image.open(BytesIO(contents))

    # transform the image
    trans_image: Tensor = transform(image).unsqueeze(0)

    # perform inference
    with torch.no_grad():
        output = model(trans_image).squeeze(0)
        predicted = F.softmax(output)
    sorted_values = predicted.argsort(descending=True).cpu().numpy()

    # return the top 10 predictions (at most 10)
    top10pred = list(
        map(
            lambda x: {
                "class_idx": x.item(),
                "class_name": idx_to_classname[str(x)],
                "confidence": predicted[x].item(),
            },
            sorted_values,
        )
    )[:10]

    logger.info(top10pred)

    return top10pred
