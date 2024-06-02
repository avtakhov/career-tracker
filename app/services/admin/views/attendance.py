import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import User, UsersGroups


async def get_users(group_name: str, session: AsyncSession) -> list[User]:
    result = await session.execute(
        sqla.select(User)
        .join(UsersGroups, onclause=UsersGroups.user_id == User.user_id)
        .where(group_name == UsersGroups.group_name)
    )
    return list(result.scalars().all())


async def add_amount(user_ids: list[int], reward: int, session: AsyncSession):
    await session.execute(
        sqla.update(User)
        .where(User.user_id.in_(user_ids))
        .values({User.amount: User.amount + reward})
    )
