from pydantic import BaseModel


class Msg(BaseModel):
    msg: str


class TaskId(BaseModel):
    taskId: str
