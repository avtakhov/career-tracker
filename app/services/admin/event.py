import sqladmin
import wtforms
from sqladmin.fields import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
import sqlalchemy as sqla

from app.core.db.base import sync_session
from app.services.admin.views.group_list import GroupList
from app.services.bot.models import Group
from app.services.bot.models.event import Event


class EventForm(wtforms.Form):
    event_name = wtforms.StringField(render_kw={"class": "form-control"})
    description = wtforms.TextAreaField(render_kw={"class": "form-control"})
    group_name = QuerySelectField(
        query_factory=GroupList.get,
        get_pk=GroupList.get_pk,
        get_label=GroupList.get_label,
        render_kw={"class": "form-control"},
    )
    reward = wtforms.IntegerField(render_kw={"class": "form-control"})
    date = DateField(render_kw={"class": "form-control"})


class EventAdmin(sqladmin.ModelView, model=Event):
    column_list = [Event.event_name, Event.date, Event.group_name]
    form = EventForm
