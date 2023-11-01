from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.requests import Request
from starlette.routing import Route, Mount
import json
import time


async def application(request: Request) -> JSONResponse:
    print(f"REQUEST: {dir(request)}")
    response = {"message": "application"}
    return JSONResponse(response)


async def dummy(request: Request) -> JSONResponse:
    print(f"REQUEST: {dir(request)}")
    base_url = request.base_url.components
    client = request.client
    method = request.method
    items = request.items()
    for i in items:
        print(i[0], ": ", i[1])
    body = await request.body()
    stream = request.stream()
    async for i in stream:
        print(i)
    disconnect = await request.is_disconnected()
    request.state.time_started = time.time()
    return JSONResponse(
        {
            "base_url": base_url,
            "body": json.loads(body.decode()),
            "client": client,
            "method": method,
            "disconnect": disconnect,
            "time_started": request.state.time_started
        }
    )


async def keychain(request: Request) -> JSONResponse:
    body = await request.json()
    print(body.get("key"))
    return JSONResponse(body)


routes = [
    Route("/", application),
    Route("/dummy", dummy, methods=["POST"]),
    Route("/keychain", keychain, methods=["POST"]),
]
