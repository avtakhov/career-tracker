import telegram.ext
from telegram.ext import ApplicationBuilder

from .services.bot.config import bot_handlers
from .settings import settings

_application: telegram.ext.Application | None = None


def get_telegram_application() -> telegram.ext.Application:
    global _application
    if _application is None:
        _application = (
            ApplicationBuilder()
            .token(settings.telegram_token)
            .build()
        )

        _application.add_handlers(bot_handlers)

    return _application
