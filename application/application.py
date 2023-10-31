from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.requests import Request
from starlette.routing import Route, Mount

async def application(request:Request) -> JSONResponse:
    print(f"REQUEST: {dir(request)}")
    response = {"message": "application"}
    return JSONResponse(response)

async def keychain(request:Request) -> JSONResponse:
    body = await request.json() 
    print(body.get("key"))
    return JSONResponse(body)

routes = [
    Route("/", application),
    Route("/keychain", keychain, methods=["POST"])
]