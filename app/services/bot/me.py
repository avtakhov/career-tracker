from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from app.core.db.base import async_session
from .views.common import get_user_groups, get_user
from .views.me import get_purchased_products


async def me(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    async with async_session() as session:
        user = await get_user(update.effective_user.id, session)
        if user is None:
            await update.message.reply_text("Мне про вас ничего неизвестно :(")
            return
        groups = await get_user_groups(user.user_id, session)
        products = [
            escape_markdown(product, version=2)
            for product in await get_purchased_products(user.user_id, session)
        ]

        await update.message.reply_text(
            f'_Пользователь:_ {escape_markdown(user.full_name, version=2)}\n' +
            f'_Баланс:_ {user.amount}\n' +
            f'_Группы:_ {", ".join(escape_markdown(group, version=2) for group in groups)}' +
            (
                f'\n\n_Необработанные покупки:_\n{ ", ".join(products) }'
                if products else ""
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
