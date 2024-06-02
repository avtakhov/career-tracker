import typing

import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import UsersGroups


async def clear_user_groups(user_id: int, session: AsyncSession):
    await session.execute(
        sqla.delete(UsersGroups)
        .where(UsersGroups.user_id == user_id)
    )


async def add_user_groups(user_id: int, groups: typing.Iterable[str], session: AsyncSession):
    await session.execute(
        sqla.insert(UsersGroups)
        .values([{"user_id": user_id, "group_name": group_name} for group_name in groups])
    )
