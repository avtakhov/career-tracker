import typing

import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import Event, UsersGroups, Chat


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
