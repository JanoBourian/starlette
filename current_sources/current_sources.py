from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
import main


async def get_current_sources(request: Request) -> JSONResponse:
    print(request)
    query = main.sources.select()
    results = await main.database.fetch_all(query)
    content = [
        {
            "uuid": result["uuid"],
            "name": result["name"],
            "current_amount": result["current_amount"],
        }
        for result in results
    ]
    return JSONResponse(content)


async def add_current_source(request: Request) -> JSONResponse:
    print(request)
    data = await request.json()
    query = main.sources.insert().values(
        name=data["name"],
        current_amount=data["current_amount"],
    )
    await main.database.execute(query)
    return JSONResponse(
        {"name": data["name"], "current_amount": data["current_amount"]}
    )


routes = [
    Route("/", get_current_sources, methods=["GET"]),
    Route("/add", add_current_source, methods=["POST"]),
]
