import sqladmin

from app.services.bot.models.user import User


class UserAdmin(sqladmin.ModelView, model=User):
    column_list = [User.full_name, User.amount, User.telegram_username]
    form_columns = [User.full_name, User.amount, User.telegram_username]
    column_searchable_list = [User.full_name]
