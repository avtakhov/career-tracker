import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import User, Chat


async def get_new_user(telegram_username: str, session: AsyncSession) -> User | None:
    result = await session.execute(
        sqla.select(User)
        .filter(User.telegram_username == telegram_username)
    )

    return result.scalar_one_or_none()


async def insert_new_chat(telegram_user_id: int, user_id: int, session: AsyncSession):
    await session.execute(
        sqla.insert(Chat),
        [
            {"telegram_user_id": telegram_user_id, "user_id": user_id, }
        ]
    )
