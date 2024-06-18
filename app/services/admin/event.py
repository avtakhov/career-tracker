import sqladmin
import wtforms
from sqladmin.fields import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
import sqlalchemy as sqla

from app.core.db.base import sync_session
from app.services.admin.views.group_list import GroupList
from app.services.bot.models import Group
from app.services.bot.models.event import Event


class EventAdmin(sqladmin.ModelView, model=Event):
    icon = "fa-solid fa-calendar"
    name_plural = "Мероприятия"
    form_columns = [Event.event_name, Event.description, Event.group, Event.reward, Event.date]
    column_labels = {
        Event.event_name: "Название",
        Event.description: "Описание",
        Event.group: "Группа",
        Event.reward: "Награда",
        Event.date: "Дата",
    }
    can_export = False
    form_overrides = {
        "description": wtforms.TextAreaField,
    }
    column_list = [Event.event_name, Event.date, Event.group_name]
