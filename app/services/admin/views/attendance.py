import sqlalchemy as sqla
import telegram
from sqlalchemy.ext.asyncio import AsyncSession
from telegram.constants import ParseMode

from app.core.db.base import async_session
from app.services.bot.models import User, UsersGroups, Chat
from app.telegram_application import get_telegram_application


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


async def get_user_info(user_ids: list[int], session: AsyncSession) -> list[tuple]:
    result = await session.execute(
        sqla.select(Chat.telegram_user_id, User.amount)
        .join(User, onclause=User.user_id == Chat.user_id)
        .where(User.user_id.in_(user_ids))
    )

    return [(chat_id, amount) for (chat_id, amount, ) in result.all()]


async def notify_users(user_ids: list[int], reward: int):
    users: list[tuple]
    async with async_session() as session:
        users = await get_user_info(user_ids, session)

    bot: telegram.Bot = get_telegram_application().bot
    for (chat_id, amount,) in users:
        try:
            await bot.send_message(
                chat_id,
                f"Начислено {reward} 🟡\n_Баланс:_ {amount}",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        except telegram.error.TelegramError:
            pass
