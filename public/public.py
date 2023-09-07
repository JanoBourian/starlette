from starlette.requests import Request
from starlette.routing import Route
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def index_page(request: Request):
    print(request)
    information = {"name": "janobourian"}
    return templates.TemplateResponse(
        "index.html", {"request": request, "information": information}
    )


routes = [Route("/", index_page)]
