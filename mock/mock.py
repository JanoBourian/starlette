from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.websockets import WebSocket
from starlette.staticfiles import StaticFiles
import asyncio


async def home(request: Request) -> JSONResponse:
    print(dir(request.app))
    print(dir(request.app.middleware))
    print(dir(request.app.state))
    print(f"GENERIC INFORMATION: {app.state.DUMMY_VALUE}")
    return JSONResponse({"message": "hello"})


async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, my friend!")
    await asyncio.sleep(2)
    print(f"GENERIC INFORMATION: {app.state.DUMMY_VALUE}")
    await websocket.close()


async def startup():
    app.state.DUMMY_VALUE = "dummy value"
    print("Starting...")


async def shutdown():
    print(f"GENERIC INFORMATION: {app.state.DUMMY_VALUE}")
    print("Shutting down...")


routes = [
    Route("/", home, methods=["GET"]),
    WebSocketRoute("/ws", websocket),
    Mount("/static", StaticFiles(directory="static")),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup], on_shutdown=[shutdown])
