import typing

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.core.db.base import async_session
from app.core.markdown import markdown_escape
from .models import Event
from .views.events import get_events


def event_to_string(event: Event):
    date_str = event.date.strftime("%d\\.%m\\.%Y")
    return f'📌 {date_str} *{markdown_escape(event.event_name)}*:\n{markdown_escape(event.description)}'


async def events(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
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
