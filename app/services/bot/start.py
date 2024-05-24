from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.ext import ContextTypes
import sqlalchemy as sqla

from app.core.db.base import async_session
from .models import *
from .views.common import get_user_groups


async def get_known_user(telegram_user_id: int, session: AsyncSession):
    result: sqla.Result = await session.execute(
        sqla.select(User)
        .join(Chat, Chat.user_id == User.user_id)
        .filter(
            Chat.telegram_user_id == telegram_user_id
        )
    )

    return result.scalar_one_or_none()


async def get_new_user(telegram_username: str, session: AsyncSession) -> User | None:
    result = await session.execute(
        sqla.select(User)
        .filter(User.telegram_username == telegram_username)
    )

    return result.scalar_one_or_none()


async def insert_new_chat(telegram_user_id: int, user_id: int, session: AsyncSession):
    await session.execute(
        sqla.insert(Chat),
        [
            dict(telegram_user_id=telegram_user_id, user_id=user_id),
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with async_session() as session:
        known = await get_known_user(update.effective_user.id, session)
        if known is not None:
            groups = await get_user_groups(known.user_id, session)
            await update.message.reply_text(f"Снова здравствуй, {known.full_name}.\nГруппы: {', '.join(groups)}.")
            return

        new_user = await get_new_user(update.effective_user.username, session)
        if new_user is None:
            await update.message.reply_text("Я вас не знаю, свяжитесь с администратором")
            return

        await insert_new_chat(update.effective_user.id, new_user.user_id, session)
        await session.commit()
        groups = await get_user_groups(new_user.user_id, session)
        await update.message.reply_text(f"Привет, {new_user.full_name}!\nГруппы: {', '.join(groups)}.")
