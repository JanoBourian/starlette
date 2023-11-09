from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.requests import Request
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.convertors import Convertor, register_url_convertor
from datetime import datetime
import json
from accounts import accounts
from application import application
from home import home
from wbsockets import wbsockets
from chat import chat
from public import public
from example import example
from current_sources import current_sources

## Configuration for database connection
import contextlib
import databases
import sqlalchemy
from starlette.config import Config

config = Config(".env")
DATABASE_URL = config("DATABASE_URL")

# Database table definitions.
metadata = sqlalchemy.MetaData()

sources = sqlalchemy.Table(
    "sources",
    metadata,
    sqlalchemy.Column("uuid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("current_amount", sqlalchemy.Float),
    sqlalchemy.Column("image", sqlalchemy.LargeBinary),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("modified_at", sqlalchemy.DateTime),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime),
)

database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()


class DateTimeConvertor(Convertor):
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(.[0-9]+)?"

    def convert(self, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

    def to_string(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%dT%H:%M:%S")


register_url_convertor("datetime", DateTimeConvertor())


async def homepage(request):
    print(f"REQUEST: {request}")
    print(f"REQUEST INFORMATION: {dir(request)}")
    print(f"HEADERS: {request.headers}")
    print(f"QUERY PARAMS: {request.query_params}")
    print(f"REQUEST.APP: {request.app}")
    print(f"REQUEST.APP INFORMATION: {dir(request.app)}")
    return JSONResponse({"hello": "world"})


async def user_me(request):
    print(f"REQUEST: {request}")
    username = "Janobourian"
    return PlainTextResponse("Hello %s!" % username)


async def user(request):
    username = request.path_params.get("username", None)
    return PlainTextResponse("Hello %s!" % username)


async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text("Hello, websocket!")
    await websocket.close()


async def get_path(request: Request):
    path_str = request.path_params.get("rest_of_path")
    print(request.path_params)
    return JSONResponse({"path": path_str})


async def get_time(request: Request):
    history = request.path_params.get("date", None)
    print(request.path_params)
    return JSONResponse({"history": str(history)})


async def get_info(request):
    print(dir(request))
    if request.method == "GET":
        content = json.dumps({"user": "user"})
        return Response(content=content, status_code=200)
    elif request.method == "POST":
        return JSONResponse({"item": "item was added!"}, status_code=201)
    else:
        return JSONResponse(
            {"error": "Invalid method or invalid operation!"}, status_code=400
        )


def startup():
    print("Ready to go!")


routes = [
    Route("/", homepage),
    Route("/user/me", user_me),
    Route("/user/{username}", user),
    Route("/path/{rest_of_path:path}", get_path),
    Route("/history/{date:datetime}", get_time),
    WebSocketRoute("/ws", websocket_endpoint),
    Mount("/static", StaticFiles(directory="static")),
    Mount(
        "/information",
        routes=[
            Route("/user", get_info, methods=["GET", "POST", "PUT"]),
        ],
    ),
    Mount("/accounts", routes=accounts.routes),
    Mount("/home", routes=home.routes),
    Mount("/websockets", routes=wbsockets.routes),
    Mount("/chat", routes=chat.routes),
    Mount("/index", routes=public.routes),
    Mount("/example", routes=example.routes),
    Mount("/application", routes=application.routes),
    Mount("/current_sources", routes=current_sources.routes),
]

app = Starlette(
    debug=False,
    routes=routes,
    lifespan=lifespan,
)  # on_startup=[startup], lifespan=lifespan,)
