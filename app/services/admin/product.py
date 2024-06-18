import fastapi
import sqladmin
from sqladmin import action
from starlette.requests import Request

from app.core.db.base import async_session
from app.services.admin.views.product import set_zero_items
from app.services.bot.models.product import Product


class ProductAdmin(sqladmin.ModelView, model=Product):
    column_list = [Product.name, Product.cost]
    form_columns = [Product.name, Product.cost]
    name_plural = "Сувениры"
    icon = "fa-solid fa-gift"
    can_export = False

    can_edit = False
    column_default_sort = ("remaining_items", True)
    column_labels = {
        Product.name: "Название",
        Product.cost: "Стоимость",
    }

