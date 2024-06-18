import sqladmin
from wtforms import widgets
import sqlalchemy as sqla
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from app.core.db.base import sync_session, async_session
from app.services.admin.views.user import clear_user_groups, add_user_groups
from app.services.bot.models import UsersGroups, Group
from app.services.bot.models.user import User


class Groups:
    @staticmethod
    def get_groups() -> list[str]:
        with sync_session() as session:
            return session.execute(
                sqla.select(Group.group_name)
            ).scalars()


class BooleanTableField(QuerySelectMultipleField):
    widget = widgets.TableWidget()
    option_widget = widgets.CheckboxInput()
    _formdata: set

    def __init__(self, **kwargs):
        kwargs["render_kw"] = {}
        super().__init__(**kwargs)

    def process_data(self, data):
        self._formdata = set(group.group_name for group in data)


class UserAdmin(sqladmin.ModelView, model=User):
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_list = [User.full_name, User.amount, User.telegram_username]
    form_columns = [User.full_name, User.amount, User.telegram_username, User.groups]
    column_labels = {
        User.full_name: "ФИО",
        User.amount: "Баланс",
        User.telegram_username: "Telegram username",
        User.groups: "Группы",
    }
    can_export = False
    form_overrides = {
        "groups": BooleanTableField,
    }
    form_args = {
        "groups": dict(query_factory=Groups.get_groups, get_pk=lambda x: x)
    }
    form_ajax_refs = {
        "groups": {'fields': ('group_name',)}
    }
    column_searchable_list = [User.full_name]
    edit_template = "user/edit.html.jinja"
    create_template = "user/create.html.jinja"

    async def after_model_change(self, data: dict, user: User, *args) -> None:
        groups = data.get("groups")

        async with async_session() as session:
            await clear_user_groups(user.user_id, session)
            if groups:
                await add_user_groups(user.user_id, groups, session)
            await session.commit()
