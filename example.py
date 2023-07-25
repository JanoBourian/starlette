from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

async def homepage(request):
    print(f"REQUEST: {request}")
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
    await websocket.send_text('Hello, websocket!')
    await websocket.close()

def startup():
    print("Ready to go!")

routes = [
        Route("/", homepage),
        Route("/user/me", user_me),
        Route("/user/{username}", user),
        WebSocketRoute('/ws', websocket_endpoint),
        Mount('/static', StaticFiles(directory="static")),
    ]

app = Starlette(
    debug = True,
    routes = routes,
    on_startup = [startup]
)
