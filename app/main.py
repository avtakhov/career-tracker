from contextlib import asynccontextmanager
from typing import Annotated

import fastapi
from fastapi import FastAPI
from sqladmin import Admin
from telegram import Update
from telegram.ext import ApplicationBuilder

from .core.admin.auth import AdminAuth
from .core.db.base import get_engine
from .services.admin.config import admin_views, custom_views
from .services.bot.config import bot_handlers
from .settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()

app = FastAPI(lifespan=lifespan)

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

ptb = (
    ApplicationBuilder()
    .token(settings.telegram_token)
    .build()
)

for handler in bot_handlers:
    ptb.add_handler(handler)


@app.post("/")
async def process_update(
        request: fastapi.Request,
        x_telegram_bot_api_secret_token: Annotated[str, fastapi.Header()]
):
    if settings.webhook_secret_token != x_telegram_bot_api_secret_token:
        raise fastapi.HTTPException(401)
    await ptb.process_update(
        Update.de_json(await request.json(), ptb.bot)
    )
    return fastapi.Response(status_code=200)


@app.get("/favicon.ico")
async def favicon(_: fastapi.Request):
    return fastapi.responses.FileResponse("favicon.ico")
