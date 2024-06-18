import fastapi.responses
import starlette.requests
from sqladmin import BaseView, expose, ModelView, action

from app.core.admin.auth import get_username
from app.core.db.base import async_session
from app.services.admin.views.purchase import mark_purchases
from app.services.bot.models.purchase import PurchaseStatus, Purchase


class PurchaseAdmin(ModelView, model=Purchase):
    name_plural = "Покупки"
    icon = "fa-solid fa-cart-shopping"
    column_list = [Purchase.user, Purchase.product, Purchase.status, Purchase.created_at]
    form_columns = [Purchase.user, Purchase.product, Purchase.status]
    can_export = False
    column_labels = {
        Purchase.user: "Пользователь",
        Purchase.product: "Сувенир",
        Purchase.status: "Статус",
    }
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
            await mark_purchases(purchase_ids, PurchaseStatus.Received, session)
            await session.commit()

        return fastapi.responses.RedirectResponse(
            url="/admin/purchase/list?search=ordered",
            status_code=302,
        )
