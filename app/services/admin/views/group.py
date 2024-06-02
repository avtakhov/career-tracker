import sqlalchemy as sqla
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import User, UsersGroups


async def insert_users(values: list[dict], session: AsyncSession):
    if not values:
        return

    await session.execute(
        insert(User).values(values)
        .on_conflict_do_nothing(
            constraint='unique_telegram_username',
        )
    )


async def insert_users_groups(
        values: list[dict],
        group_name: str,
        session: AsyncSession,
):
    if not values:
        return

    result = await session.execute(
        sqla.select(User.user_id)
        .filter(
            User.telegram_username.in_(i['telegram_username'] for i in values)
        )
    )

    await session.execute(
        insert(UsersGroups).values([
            dict(group_name=group_name, user_id=user_id)
            for user_id in result.scalars()
        ]).on_conflict_do_nothing()
    )
