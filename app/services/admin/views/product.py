import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import Product


async def set_zero_items(
        product_ids: list[int],
        session: AsyncSession,
):
    await session.execute(
        sqla.update(Product)
        .values({Product.remaining_items: 0})
        .where(Product.product_id.in_(product_ids))
    )
