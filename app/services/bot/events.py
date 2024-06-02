import typing

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from app.core.db.base import async_session
from .models import Event
from .views.events import get_events


def event_to_string(event: Event):
    date_str = event.date.strftime("%d\\.%m\\.%Y")
    return (
            f'📌 {date_str} *{escape_markdown(event.event_name, version=2)}*:\n' +
            f'{escape_markdown(event.description, version=2)}'
    )


async def events(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    db_events: typing.Iterable[Event]
    async with async_session() as session:
        db_events = await get_events(update.effective_user.id, session)

    if not db_events:
        await update.message.reply_text("Событий не найдено :(")
        return

    await update.message.reply_text(
        '\n\n'.join(map(event_to_string, db_events)),
        parse_mode=ParseMode.MARKDOWN_V2
    )
