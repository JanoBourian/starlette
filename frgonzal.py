from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse, FileResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
import asyncio


async def homepage(request: Request):
    print(f"request.client.host: {request.client.host}")
    return FileResponse("static/index.html")

async def index(request: Request):
    return HTMLResponse(f"<h1>Index: {request.query_params}</h1>")

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text('Hola. Soy SofIA, ¿cómo puedo apoyarte?')

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            await asyncio.sleep(0.5)
            await websocket.send_text(f"Echo: {data}")

    except Exception as e:
        print(f"WebSocket connection closed with error: {e}")
    finally:
        await websocket.close()
        
        
@asynccontextmanager
async def lifespan(app):
    print("Starting up...")
    yield
    print("Shutting down...")
    
routes=[
        Route("/", homepage),
        Route("/index", index),
        WebSocketRoute('/ws', websocket_endpoint),
        Mount('/static', StaticFiles(directory="static"))
    ]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifespan
)
