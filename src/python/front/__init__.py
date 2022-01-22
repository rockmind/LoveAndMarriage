import uvicorn
from os import getenv
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer

from starlette.middleware.wsgi import WSGIMiddleware

from mapPL_provinces import app as app_provinces
from mapPL_districts import app as app_districts
from services.base_app import get_base_rpc_app

token_auth_scheme = HTTPBearer()


server = get_base_rpc_app('FrontApp')


@server.get("/")
async def root():
    return {"message": "Hello World"}


@server.get("/districts", response_class=HTMLResponse)
def provinces():
    return app_provinces.index()


@server.get("/districts", response_class=HTMLResponse)
def districts():
    return app_districts.index()


if __name__ == "__main__":
    port = int(getenv('APP_PORT', 8000))
    server.mount("/provinces", WSGIMiddleware(app_provinces.server))
    server.mount("/districts ", WSGIMiddleware(app_districts.server))
    uvicorn.run(server, host='0.0.0.0', port=port)

