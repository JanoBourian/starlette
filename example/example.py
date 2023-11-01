from starlette.responses import JSONResponse, StreamingResponse
from starlette.requests import Request
from starlette.routing import Route, Mount, WebSocketRoute
import asyncio


async def example_get(request):
    items_app = request.app
    print(f"ITEM INFORMATION: {dir(items_app)}")
    print(f"ITEM TYPE: {type(items_app)}")
    return JSONResponse({"message": "Hello form example_get"}, status_code=200)


async def example_post(request):
    body = await request.body()
    print(f"REQUEST BODY: {body}")
    print(f"REQUEST TYPE: {type(body)}")
    return JSONResponse({"message": "Hello form example_post"}, status_code=201)


async def wsconnection(websocket):
    print(f"WEBSOCKET INFORMATION: {dir(websocket)}")
    await websocket.accept()
    await websocket.send_text("Hello, from websocket in Starlette!")
    await websocket.close()


async def request_query_params(request):
    class_name = request.path_params.get("classname", "")
    query_params = request.query_params.get("days", [])
    print(f"PATH INFORMATION: {request.path_params}")
    print(f"QUERY INFORMATION: {request.query_params}")
    return JSONResponse(
        {"class_name": class_name, "query_params": query_params}, status_code=200
    )


async def slow_numbers(minimum, maximum):
    yield "<html><body><ul>"
    for number in range(minimum, maximum + 1):
        yield "<li>%d</li>" % number
        await asyncio.sleep(0.5)
    yield "</ul></body></html>"


async def example_response(request):
    generator = slow_numbers(1, 10)
    return StreamingResponse(generator)


routes = [
    Route("/", example_get, methods=["GET"]),
    Route("/", example_post, methods=["POST"]),
    Route("/streaming", example_response),
    Route("/class/{classname}", request_query_params),
    WebSocketRoute("/ws", wsconnection),
]
