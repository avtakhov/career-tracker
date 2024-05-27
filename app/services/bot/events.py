import datetime
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import sqlalchemy as sqla

from app.core.db.base import async_session
from app.core.markdown import markdown_escape
from .models import *


async def get_events(telegram_user_id: int, session: AsyncSession) -> typing.Iterable[Event]:
    result = await session.execute(
        sqla.select(Event)
        .join(UsersGroups, Event.group_name == UsersGroups.group_name)
        .join(Chat, Chat.user_id == UsersGroups.user_id)
        .filter(Chat.telegram_user_id == telegram_user_id)
        .filter(Event.date >= sqla.func.current_date())
        .order_by(Event.date)
    )
    return result.scalars().all()


def event_to_string(event: Event):
    date_str = event.date.strftime("%d\\.%m\\.%Y")
    return f'📌 {date_str} *{markdown_escape(event.event_name)}*:\n{markdown_escape(event.description)}'


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    events: typing.Iterable[Event]
    async with async_session() as session:
        events = await get_events(update.effective_user.id, session)

    if not events:
        await update.message.reply_text("Событий не найдено :(")
        return

    await update.message.reply_text(
        '\n\n'.join(map(event_to_string, events)),
        parse_mode=ParseMode.MARKDOWN_V2
    )
