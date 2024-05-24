import pydantic
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import sqlalchemy as sqla

from app.core.db.base import async_session
from .models import *
from .models import User
from .views.common import get_user_groups
from app.core.markdown import markdown_escape


async def get_user(telegram_user_id: int, session: AsyncSession) -> User | None:
    result = await session.execute(
        sqla.select(User)
        .join(Chat, Chat.user_id == User.user_id)
        .filter(Chat.telegram_user_id == telegram_user_id)
    )

    return result.scalar_one_or_none()


async def me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with async_session() as session:
        user = await get_user(update.effective_user.id, session)
        if user is None:
            await update.message.reply_text("Мне про вас ничего неизвестно :(")
            return
        groups = await get_user_groups(user.user_id, session)

        await update.message.reply_text(
            f'__Пользователь:__ {markdown_escape(user.full_name)}\n__Баланс:__ {user.amount}\n__Группы:__ {", ".join(map(markdown_escape, groups))}',
            parse_mode=ParseMode.MARKDOWN_V2,
        )
