from starlette.requests import Request
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.responses import HTMLResponse
from starlette.routing import Route, WebSocketRoute
import time

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/chat/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class Chatpage(HTTPEndpoint):
    async def get(self, request: Request):
        print(request)
        return HTMLResponse(html)


class Echo(WebSocketEndpoint):
    encoding = "text"

    async def on_receive(self, websocket, data):
        await websocket.send_text("Response")
        await websocket.send_text(f"Message text was: {data}")


routes = [Route("/", Chatpage), WebSocketRoute("/ws", Echo)]
