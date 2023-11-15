from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


async def home(request: Request) -> JSONResponse:
    return JSONResponse({"message": "hello"})


routes = [Route("/", home, methods=["GET"])]

app = Starlette(debug=True, routes=routes)
