import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.markdown import markdown_escape
from app.services.bot.models import UsersGroups, User, Chat


async def get_user_groups(user_id: int, session: AsyncSession) -> list[str]:
    result = await session.execute(
        sqla.select(UsersGroups.group_name)
        .filter(UsersGroups.user_id == user_id)
    )

    return [group_name for (group_name, ) in result.all()]


async def get_user(telegram_user_id: int, session: AsyncSession) -> User | None:
    result = await session.execute(
        sqla.select(User)
        .join(Chat, Chat.user_id == User.user_id)
        .filter(Chat.telegram_user_id == telegram_user_id)
    )

    return result.scalar_one_or_none()

