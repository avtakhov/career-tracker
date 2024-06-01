from telegram.ext import CommandHandler, CallbackQueryHandler

from .start import start
from .events import events
from .me import me
from .products import products, products_get, products_list, products_purchase

bot_handlers = [
    CommandHandler("start", start),
    CommandHandler("events", events),
    CommandHandler("me", me),
    CommandHandler("products", products),
    CallbackQueryHandler(products_get, "^products/get"),
    CallbackQueryHandler(products_list, "^products/list"),
    CallbackQueryHandler(products_purchase, "^products/purchase"),
]
