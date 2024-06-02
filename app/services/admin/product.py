import fastapi
import sqladmin
from sqladmin import action
from starlette.requests import Request

from app.core.db.base import async_session
from app.services.admin.views.product import set_zero_items
from app.services.bot.models.product import Product


class ProductAdmin(sqladmin.ModelView, model=Product):
    column_list = [Product.name, Product.cost, Product.remaining_items]
    form_columns = [Product.name, Product.cost, Product.remaining_items]

    can_edit = False
    column_default_sort = ("remaining_items", True)

    @action("zero_items", "Set remaining_items to 0")
    async def zero_items(self, request: Request):
        product_ids = self.parse_pks(request)
        async with async_session() as session:
            await set_zero_items(product_ids, session)
            await session.commit()

        return fastapi.responses.RedirectResponse(
            url="/admin/product/list",
            status_code=302,
        )

    def parse_pks(self, request: Request) -> list[int]:
        pks = request.query_params.get("pks")
        if not pks:
            return []

        return list(map(int, pks.split(",")))
