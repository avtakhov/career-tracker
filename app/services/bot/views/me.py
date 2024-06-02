import typing

import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import Purchase, Product
from app.services.bot.models.purchase import PurchaseStatus


async def get_purchased_products(user_id: int, session: AsyncSession) -> typing.Iterable[str]:
    result = await session.execute(
        sqla.select(Product.name)
        .join(Purchase, onclause=Purchase.product_id == Product.product_id)
        .order_by(Purchase.created_at)
        .where(Purchase.user_id == user_id)
        .where(Purchase.status == PurchaseStatus.Ordered)
    )
    return result.scalars().all()
