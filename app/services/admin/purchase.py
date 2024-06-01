import typing

import fastapi.responses
import pydantic
import sqlalchemy as sqla
import starlette.requests
import wtforms
from sqladmin import BaseView, expose, ModelView, action
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin.auth import get_username
from app.core.db.base import async_session
from app.services.bot.models import User, Product
from app.services.bot.models.purchase import PurchaseStatus, Purchase


async def mark(
        purchase_ids: list[int],
        status: PurchaseStatus,
        session: AsyncSession,
):
    await session.execute(
        sqla.update(Purchase)
        .values({Purchase.status: status})
        .where(Purchase.purchase_id.in_(purchase_ids))
    )


class PurchaseAdmin(ModelView, model=Purchase):

    column_list = [Purchase.user, Purchase.product, Purchase.status, Purchase.created_at]
    column_searchable_list = [Purchase.status]
    form_ajax_refs = {
        "product": {
            "fields": ("name",),
        },
        "user": {
            "fields": ("full_name",)
        }
    }

    def is_accessible(self, request: starlette.requests.Request) -> bool:
        token = request.session.get("token")
        if not token or get_username(token) is None:
            raise fastapi.HTTPException(status_code=401)
        return True

    def parse_pks(self, request: starlette.requests.Request) -> list[int]:
        pks = request.query_params.get("pks")
        if not pks:
            return []

        return list(map(int, pks.split(",")))

    @action("mark-received", "Mark received")
    async def mark_received(self, request: starlette.requests.Request):
        purchase_ids = self.parse_pks(request)
        async with async_session() as session:
            await mark(purchase_ids, PurchaseStatus.Received, session)
            await session.commit()

        return fastapi.responses.RedirectResponse(
            url="/admin/purchase/list?search=ordered",
            status_code=302,
        )
