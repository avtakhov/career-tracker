from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from sqladmin import Admin
from telegram import Update
from telegram.ext import ApplicationBuilder

from .core.admin.auth import AdminAuth
from .core.db.base import get_engine
from .services.admin.config import admin_views
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
    authentication_backend=AdminAuth(settings.secret_key)
)
for item in admin_views:
    admin.add_view(item)

ptb = (
    ApplicationBuilder()
    .token(settings.telegram_token)
    .build()
)

for handler in bot_handlers:
    ptb.add_handler(handler)


@app.post("/")
async def process_update(request: fastapi.Request):
    req = await request.json()
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return fastapi.Response(status_code=200)
