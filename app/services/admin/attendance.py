import fastapi.responses
import sqlalchemy as sqla
import starlette.requests
import wtforms
from sqladmin import BaseView, expose
from sqlalchemy.ext.asyncio import AsyncSession
from wtforms.fields.simple import HiddenField
from wtforms_sqlalchemy.fields import QuerySelectField

from app.core.admin.auth import get_username
from app.core.db.base import async_session
from app.services.admin.views.attendance import get_users, add_amount
from app.services.admin.views.event_list import EventList
from app.services.bot.models import Event, User, UsersGroups


class UserForm(wtforms.Form):
    user = wtforms.BooleanField()
    user_id = HiddenField()


class GroupForm(wtforms.Form):
    users = wtforms.FieldList(wtforms.FormField(UserForm))
    reward = HiddenField()
    submit = wtforms.SubmitField()


class EventForm(wtforms.Form):
    select = QuerySelectField(
        query_factory=EventList.get_events,
        get_pk=EventList.get_pk,
        get_label=EventList.get_label,
        render_kw={"class": "form-control"},
    )
    submit = wtforms.SubmitField(label="Choose")


class AttendanceAdmin(BaseView):
    name = "Attendance"
    icon = "fa-solid fa-chart-line"

    @expose("/attendance", methods=["GET", "POST"])
    async def attendance_page(self, request: starlette.requests.Request):
        if request.method == "GET":
            return self.templates.TemplateResponse(
                request,
                "attendance/event_select.html.jinja",
                context={
                    'event_form': EventForm(),
                },
            )

        form_data = EventForm(await request.form())
        event: Event = form_data.select.data
        users: list[User]
        async with async_session() as session:
            users = await get_users(event.group_name, session)

        group_form = GroupForm()
        group_form.reward.data = str(event.reward)
        for user in users:
            group_form.users.append_entry(UserForm())
            user_form: UserForm = group_form.users.entries[-1]
            user_form.user.label.text = f"{user.full_name}"
            user_form.user_id.data = str(user.user_id)

        return self.templates.TemplateResponse(
            request,
            "attendance/group.html.jinja",
            context={
                'group_form': group_form,
            },
        )

    @expose("/attendance/group", methods=["POST"])
    async def event_chose(self, request: starlette.requests.Request):
        form_data = GroupForm(await request.form())
        user_ids = [int(user_form.user_id.data) for user_form in form_data.users.entries if user_form.user.data]
        reward = int(form_data.reward.data)
        async with async_session() as session:
            await add_amount(user_ids, reward, session)
            await session.commit()
        return fastapi.responses.RedirectResponse(url="/admin/attendance", status_code=302)

    def is_accessible(self, request: starlette.requests.Request) -> bool:
        token = request.session.get("token")
        if not token or get_username(token) is None:
            raise fastapi.HTTPException(status_code=401)
        return True
