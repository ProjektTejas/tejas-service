from io import BytesIO
from typing import Dict, Any

import torch
import torchvision.transforms as T
import torch.nn.functional as F

from PIL import Image
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from torch import Tensor
from torch.jit import ScriptModule


router = APIRouter()


class ClassifyModelMeta(BaseModel):
    modelName: str
    modelPath: str
    idxToClassname: Dict[int, str]


@router.post("/classify")
async def classify_image(
    *, model_meta: ClassifyModelMeta = Form(...), file: UploadFile = File(...)
):
    model: ScriptModule = torch.jit.load(model_meta.modelPath)

    if model_meta.modelName == "mobilenet_v2":
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
    image = Image.open(BytesIO(contents))

    trans_image: Tensor = transform(image).unsqueeze(0)

    # perform inference
    with torch.no_grad():
        output = model(trans_image).squeeze(0)
        predicted = F.softmax(output)
    sorted_values = predicted.argsort(descending=True).cpu().numpy()

    top10pred = list(
        map(
            lambda x: {
                "class_idx": x.item(),
                "class_name": model_meta.idxToClassname[x],
                "confidence": predicted[x].item(),
            },
            sorted_values,
        )
    )[:10]

    return top10pred
