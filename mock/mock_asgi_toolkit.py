from starlette.responses import PlainTextResponse

async def app(scope, receive, send):
    assert scope["type"] == "http"
    print(f"SCOPE: {scope}")
    print(f"RECEIVE: {receive}")
    print(f"TYPE_RECEIVE: {dir(receive)}")
    print(f"SEND: {send}")
    print(f"TYPE_SEND: {dir(send)}")
    response = PlainTextResponse("Hello, world!")
    await response(scope, receive, send)