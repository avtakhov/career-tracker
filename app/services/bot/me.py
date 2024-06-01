from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.core.db.base import async_session
from .views.common import get_user_groups, get_user
from app.core.markdown import markdown_escape


async def me(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    async with async_session() as session:
        user = await get_user(update.effective_user.id, session)
        if user is None:
            await update.message.reply_text("Мне про вас ничего неизвестно :(")
            return
        groups = await get_user_groups(user.user_id, session)

        await update.message.reply_text(
            f'__Пользователь:__ {markdown_escape(user.full_name)}\n' +
            f'__Баланс:__ {user.amount}\n' +
            f'__Группы:__ {", ".join(map(markdown_escape, groups))}',
            parse_mode=ParseMode.MARKDOWN_V2,
        )
