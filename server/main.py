import os
import oauth2
from routers import api, optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    openapi_url="/mango/openapi.json",
    redoc_url="/mango/redoc/",
    docs_url="/mango/docs"
)
script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")

origins = [
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://www.mangoconsultant.net",
    "https://mangoserverbot.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["/api/*"],
    allow_headers=["/api/*"],
)

app.include_router(
    oauth2.router,
    prefix='/api/authentication',
    tags=['Authentication'],
)

app.include_router(
    api.router,
    prefix="/api/line"
)

app.include_router(
    optional.router,
    prefix='/api/optional'
)

description = """
SERVER BOT APP API helps you do awesome stuff. 🚀

## APIs

You can **read items each API**.

You will be able to:


***OpenAPI Public only prefix /api**
"""


def custom_openapi():
    """
    docs description API
    :return:
        -> func
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Mango-Server Notification",
        version="2.0.0",
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
