from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import JSONResponse


async def get_current_sources(request: Request) -> JSONResponse:
    print(request)
    return JSONResponse({"message": "Hello from current_inputs"})


routes = [
    Route("/", get_current_sources, methods=["GET"]),
]
