import sqladmin

from app.services.bot.models.product import Product


class ProductAdmin(sqladmin.ModelView, model=Product):
    column_list = [Product.name, Product.cost]
    form_columns = [Product.name, Product.cost]
