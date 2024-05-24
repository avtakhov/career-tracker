import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.markdown import markdown_escape
from app.services.bot.models import UsersGroups


async def get_user_groups(user_id: int, session: AsyncSession) -> list[str]:
    result = await session.execute(
        sqla.select(UsersGroups.group_name)
        .filter(UsersGroups.user_id == user_id)
    )

    return [group_name for (group_name, ) in result.all()]
