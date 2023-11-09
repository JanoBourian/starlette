from starlette.applications import Starlette
from starlette.responses import (
    PlainTextResponse,
    JSONResponse,
    StreamingResponse,
    Response,
)
from starlette.requests import Request
from starlette.routing import Route, Mount
import json
import time
import asyncio


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
            "time_started": request.state.time_started,
        }
    )


async def keychain(request: Request) -> JSONResponse:
    body = await request.json()
    print(body.get("key"))
    return JSONResponse(body)


async def fake_video_streamer():
    for _ in range(10):
        yield b"some fake video bytes"
        await asyncio.sleep(1)


async def get_video(request: Request) -> StreamingResponse:
    return StreamingResponse(fake_video_streamer())


async def set_cookie_endpoint(request: Request) -> JSONResponse:
    key_ = "dardo"
    value_ = "589"
    response = JSONResponse({"cookie": {"key": key_, "value": value_}})
    response.set_cookie(key_, value_, max_age=30)
    return response


async def slow_numbers(minimum, maximum):
    yield "<html><body><ul>"
    for number in range(minimum, maximum + 1):
        yield "<li>%d</li>" % number
        await asyncio.sleep(0.5)
    yield "</ul></body></html>"


async def numbers(request: Request) -> StreamingResponse:
    generator = slow_numbers(1, 10)
    response = StreamingResponse(generator, media_type="text/html")
    return response


routes = [
    Route("/", application),
    Route("/dummy", dummy, methods=["POST"]),
    Route("/video", get_video),
    Route("/cookie", set_cookie_endpoint, methods=["GET"]),
    Route("/numbers", numbers),
    Route("/keychain", keychain, methods=["POST"]),
]
