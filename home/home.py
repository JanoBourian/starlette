from starlette.responses import JSONResponse, PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.routing import Route
import json


class Home(HTTPEndpoint):
    async def get(self, request: Request):
        return PlainTextResponse("Hello, world!", status_code=200)

    async def post(self, request: Request):
        body = await request.json()
        return JSONResponse(json.dumps(body), status_code=201)

    async def put(self, request: Request):
        body = await request.json()
        return JSONResponse(body, status_code=201)

    async def delete(self, request: Request):
        return JSONResponse({"message": "object was deleted"}, status_code=201)


routes = [Route("/", Home)]
