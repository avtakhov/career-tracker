from telegram.ext import CommandHandler

from .start import start
from .events import events
from .me import me

bot_handlers = [
    CommandHandler("start", start),
    CommandHandler("events", events),
    CommandHandler("me", me),
]
