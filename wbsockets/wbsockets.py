from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, WebSocketRoute
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.websockets import WebSocket
import logging 

class WbSocketCommunication(WebSocketEndpoint):
    encoding = "bytes"
    
    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()

        logging.warning(f"Connected: {websocket}")

    async def on_receive(self, websocket: WebSocket, data: bytes):
        await websocket.send_bytes(b"OK!")

        logging.warning("websockets.received")

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        logging.warning(f"Disconnected: {websocket}")
    

routes = [
    WebSocketRoute("/", WbSocketCommunication)
]