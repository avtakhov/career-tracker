import datetime
import typing

import sqlalchemy as sqla
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models import Product, Purchase, User, Chat
from app.services.bot.models.purchase import PurchaseStatus


async def get_products(limit: int, offset: int, session: AsyncSession) -> typing.Iterable[Product]:
    result = await session.execute(
        sqla.select(Product)
        .order_by(Product.name)
        .limit(limit)
        .offset(offset)
        .where(sqla.or_(Product.remaining_items > 0, Product.remaining_items.is_(None)))
    )
    return result.scalars().all()


async def get_product_by_id_locked(product_id: int, session: AsyncSession) -> Product:
    result = await session.execute(
        sqla.select(Product)
        .with_for_update()
        .filter(Product.product_id == product_id)
    )
    return result.scalar_one()


async def get_product_by_id(product_id: int, session: AsyncSession) -> Product:
    result = await session.execute(
        sqla.select(Product)
        .filter(Product.product_id == product_id)
    )
    return result.scalar_one()


async def insert_purchase(user_id: int, product_id: int, session: AsyncSession):
    await session.execute(
        sqla.insert(Purchase)
        .values(
            [{
                'product_id': product_id,
                'user_id': user_id,
                'created_at': datetime.datetime.utcnow(),
                'status': PurchaseStatus.Ordered,
            }]
        )
    )


async def decrease_amount(user_id: int, cost: int, session: AsyncSession):
    await session.execute(
        sqla.update(User)
        .values({User.amount: User.amount - cost})
        .where(User.user_id == user_id)
    )


async def decrease_remaining_items(product_id: int, session: AsyncSession):
    await session.execute(
        sqla.update(Product)
        .values({Product.remaining_items: Product.remaining_items - 1})
        .where(Product.product_id == product_id)
        .where(Product.remaining_items is not None)
    )
