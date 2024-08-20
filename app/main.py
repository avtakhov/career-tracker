from contextlib import asynccontextmanager
from typing import Annotated

import fastapi
import telegram.ext
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from telegram import Update

from .telegram_application import get_telegram_application
from .core.admin.auth import AdminAuth
from .core.db.base import get_engine
from .services.admin.config import admin_views, custom_views
from .settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    application = get_telegram_application()
    async with application:
        await application.start()
        yield
        await application.stop()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

admin = Admin(
    app,
    get_engine(),
    authentication_backend=AdminAuth(settings.secret_key),
    templates_dir="templates",
)
for item in admin_views:
    admin.add_model_view(item)
for item in custom_views:
    admin.add_base_view(item)


@app.get("/")
async def get_root():
    return fastapi.responses.RedirectResponse("/admin")


@app.post("/")
async def process_update(
        request: fastapi.Request,
        x_telegram_bot_api_secret_token: Annotated[str, fastapi.Header()],
        application: telegram.ext.Application = fastapi.Depends(get_telegram_application)
):
    if settings.webhook_secret_token != x_telegram_bot_api_secret_token:
        raise fastapi.HTTPException(401)
    await application.process_update(
        Update.de_json(await request.json(), application.bot)
    )
    return fastapi.Response(status_code=200)


@app.get("/favicon.ico")
async def favicon(_: fastapi.Request):
    return fastapi.responses.FileResponse("favicon.ico")
