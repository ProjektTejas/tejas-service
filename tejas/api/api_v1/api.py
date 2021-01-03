from fastapi import APIRouter

from .endpoints import utils, classify, train, tasks

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(classify.router, prefix="/classify", tags=["classify"])
api_router.include_router(train.router, prefix="/train", tags=["model_train"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks", "task-status"])
