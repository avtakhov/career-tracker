import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bot.models.purchase import PurchaseStatus, Purchase


async def mark_purchases(
        purchase_ids: list[int],
        status: PurchaseStatus,
        session: AsyncSession,
):
    await session.execute(
        sqla.update(Purchase)
        .values({Purchase.status: status})
        .where(Purchase.purchase_id.in_(purchase_ids))
    )
