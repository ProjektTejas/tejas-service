from typing import Any

from fastapi import APIRouter

from tejas import schemas

router = APIRouter()


@router.get("/test_server", response_model=schemas.Msg, status_code=200)
def test_server() -> Any:
    """
    Test if the server is up
    """
    return {"msg": "Server is Up !"}