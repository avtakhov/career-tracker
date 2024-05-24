import asyncio

import sqladmin
import wtforms
from sqladmin.fields import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
import sqlalchemy as sqla

from app.core.db.base import async_session, sync_session
from app.services.bot.models import Group
from app.services.bot.models.event import Event


class EventForm(wtforms.Form):
    @staticmethod
    def get_groups():
        with sync_session() as session:
            result = session.execute(
                sqla.select(Group)
            )
            return result.all()

    @staticmethod
    def get_group_name(row):
        (group, ) = row
        return group.group_name

    event_name = wtforms.StringField(render_kw={"class": "form-control"})
    description = wtforms.TextAreaField(render_kw={"class": "form-control"})
    group_name = QuerySelectField(query_factory=get_groups, get_pk=get_group_name, get_label=get_group_name, render_kw={"class": "form-control"})
    date = DateField(render_kw={"class": "form-control"})


class EventAdmin(sqladmin.ModelView, model=Event):
    column_list = [Event.event_name, Event.date, Event.group_name]
    form = EventForm

