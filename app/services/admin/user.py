from typing import Any

import sqladmin
import wtforms
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from starlette.requests import Request
from wtforms import widgets
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
import sqlalchemy as sqla

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

    def process_data(self, data):
        self._formdata = set(group.group_name for group in data)


class UserForm(wtforms.Form):
    full_name = wtforms.StringField(render_kw={"class": "form-control"})
    amount = wtforms.IntegerField(default=0, render_kw={"class": "form-control"})
    telegram_username = wtforms.StringField(render_kw={"class": "form-control"})
    groups = BooleanTableField(
        query_factory=Groups.get_groups,
        get_pk=lambda x: x,
    )


class UserAdmin(sqladmin.ModelView, model=User):
    column_list = [User.full_name, User.amount, User.telegram_username]
    form = UserForm
    column_searchable_list = [User.full_name]
    edit_template = "user/edit.html.jinja"
    create_template = "user/create.html.jinja"

    def search_placeholder(self) -> str:
        return "ФИО"

    async def after_model_change(
            self,
            data: dict,
            user: User,
            is_created: bool,
            *args,
    ) -> None:
        groups = data.get("groups")
        if not groups:
            return

        async with async_session() as session:
            await clear_user_groups(user.user_id, session)
            await add_user_groups(user.user_id, groups, session)
            await session.commit()
