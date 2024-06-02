import io

import sqladmin
import wtforms
from fastapi import UploadFile
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from app.core.db.base import async_session
from app.services.admin.views.group import insert_users, insert_users_groups
from app.services.bot.models.group import Group


class GroupForm(wtforms.Form):
    group_name = wtforms.StringField("group_name", render_kw={"class": "form-control"})
    xlsx = wtforms.FileField("xlsx", render_kw={"class": "form-control"})


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
            {'full_name': full_name.strip(), 'telegram_username': telegram_username.strip()}
            for (full_name, telegram_username) in sheet.iter_rows(min_row=2, values_only=True)
            if full_name and telegram_username
        ]
        async with async_session() as session:
            await insert_users(users, session)
            await insert_users_groups(users, group.group_name, session)
            await session.commit()
