from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.requests import Request
from starlette.routing import Route


async def get_accounts(request: Request):
    return JSONResponse(
        {"accounts": ["number 1", "number 2", "number 3", "number 4", "number 5"]},
        status_code=200,
    )


routes = [Route("/", get_accounts, methods=["GET"])]
