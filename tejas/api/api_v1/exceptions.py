from fastapi import Request
from fastapi.responses import JSONResponse


class TrainingNotCompleted(Exception):
    def __init__(self, task_id: str):
        self.task_id = task_id


