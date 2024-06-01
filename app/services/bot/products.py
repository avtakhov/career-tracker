import dataclasses
import re
import typing

import pydantic
from sqlalchemy.exc import IntegrityError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler

from app.core.db.base import async_session
from .models import Product, User
from .views.common import get_user
from .views.products import get_products, get_product_by_id, decrease_amount, insert_purchase

ELEMENTS_PER_PAGE = 30


@dataclasses.dataclass
class ProductsReply:
    text: str
    reply_markup: InlineKeyboardMarkup


async def get_products_reply(telegram_user_id: int, offset: int) -> ProductsReply:
    products_page: typing.Iterable[Product]
    user: User | None
    async with async_session() as session:
        user = await get_user(telegram_user_id, session)
        products_page = await get_products(limit=ELEMENTS_PER_PAGE, offset=offset, session=session)

    keyboard = [
        [InlineKeyboardButton(product.name, callback_data=f"products/get/id/{product.product_id}/offset/{offset}")]
        for product in products_page
    ]

    return ProductsReply(
        text=f"__Баланс:__ {user.amount if user else 0}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def products(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reply = await get_products_reply(update.effective_user.id, offset=0)
    await update.message.reply_text(
        reply.text,
        reply_markup=reply.reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def products_get(update: Update, _: ContextTypes.DEFAULT_TYPE, ) -> None:
    search_result, = re.findall('products/get/id/(\\d+)/offset/(\\d+)', update.callback_query.data)
    product_id, offset = map(int, search_result)
    product: Product
    async with async_session() as session:
        product = await get_product_by_id(product_id, session)

    keyboard = [
        [
            InlineKeyboardButton(f"⬅️", callback_data=f"products/list/offset/{offset}"),
            InlineKeyboardButton(f"{product.cost} 🟡", callback_data=f"products/purchase/id/{product_id}"),
        ],
    ]

    await update.callback_query.edit_message_text(
        (
                f"__Product:__ {product.name}\n" +
                f"__Cost:__ {product.cost}"
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def products_list(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    search_result, = re.findall('products/list/offset/(\\d+)', update.callback_query.data)
    offset = int(search_result)
    reply = await get_products_reply(update.effective_user.id, offset=offset)
    await update.callback_query.edit_message_text(
        reply.text,
        reply_markup=reply.reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def products_purchase(update: Update, _: ContextTypes.DEFAULT_TYPE):
    search_result, = re.findall('products/purchase/id/(\\d+)', update.callback_query.data)
    product_id = int(search_result)
    message_text: str

    try:
        async with async_session() as session:
            user = await get_user(update.effective_user.id, session)
            product = await get_product_by_id(product_id, session)
            await insert_purchase(user.user_id, product_id, session)
            await decrease_amount(user.user_id, product.cost, session)
            await session.commit()
        message_text = "Успех! Обратитесь к администратору для получения."
    except IntegrityError:
        message_text = "Недостаточно средств"
    except Exception as e:
        message_text = f"Ошибка [{e}] :("

    keyboard = [
        [InlineKeyboardButton(f"К списку ⬅️", callback_data=f"products/list/offset/{0}"),]
    ]

    await update.callback_query.edit_message_text(
        message_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
