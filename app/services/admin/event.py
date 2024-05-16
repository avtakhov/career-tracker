import sqladmin

from app.services.bot.models.event import Event


class EventAdmin(sqladmin.ModelView, model=Event):
    column_list = [Event.event_name, Event.date, Event.group_name]
    form_columns = [Event.event_name, Event.description, Event.date, Event.group_name]
    form_include_pk = True
