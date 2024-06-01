from telegram import Update
from telegram.ext import ContextTypes

from app.core.db.base import async_session
from .views.common import get_user_groups, get_user
from .views.start import get_new_user, insert_new_chat


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    async with async_session() as session:
        known = await get_user(update.effective_user.id, session)
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
