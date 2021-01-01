from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware

from tejas.api.api_v1.api import api_router
from tejas.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

if settings.ALLOW_ALL_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"hello", "world"}


# web sockets do not work with mangum, so we will have to halt this for now
# @app.websocket("/")
# async def websock_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was : {data}")
