import io

import sqladmin
import wtforms
import sqlalchemy as sqla
from fastapi import UploadFile
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.base import async_session
from app.services.bot.models import User, UsersGroups
from app.services.bot.models.group import Group


class GroupForm(wtforms.Form):
    group_name = wtforms.StringField("group_name", render_kw={"class": "form-control"})
    xlsx = wtforms.FileField("xlsx", render_kw={"class": "form-control"})


async def insert_users(values: list[dict], session: AsyncSession):
    if not values:
        return

    await session.execute(
        insert(User).values(values)
        .on_conflict_do_nothing(
            constraint='unique_telegram_username',
        )
    )


async def insert_users_groups(
        values: list[dict],
        group_name: str,
        session: AsyncSession,
):
    if not values:
        return

    result = await session.execute(
        sqla.select(User.user_id)
        .filter(
            User.telegram_username.in_(i['telegram_username'] for i in values)
        )
    )

    await session.execute(
        insert(UsersGroups).values([
            dict(group_name=group_name, user_id=user_id)
            for user_id in result.scalars()
        ]).on_conflict_do_nothing()
    )


class GroupAdmin(sqladmin.ModelView, model=Group):
    column_list = [Group.group_name]
    form = GroupForm
    form_include_pk = True

    async def after_model_change(self, data, group: Group, is_created: bool, *args):
        xlsx: UploadFile = data.get("xlsx")
        if xlsx.size == 0:
            return

        sheet: Worksheet = load_workbook(
            io.BytesIO(xlsx.file.read()),
            read_only=True
        ).active

        xlsx.file.close()

        users = [
            {'full_name': full_name, 'telegram_username': telegram_username}
            for (full_name, telegram_username) in sheet.iter_rows(min_row=2, values_only=True)
        ]
        async with async_session() as session:
            await insert_users(users, session)
            await insert_users_groups(users, group.group_name, session)
            await session.commit()
