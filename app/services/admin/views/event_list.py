import sqlalchemy as sqla

from app.core.db.base import sync_session
from app.services.bot.models import Event


class EventList:
    @staticmethod
    def get():
        with sync_session() as session:
            result = session.execute(
                sqla.select(Event)
            )
            return result.scalars().all()

    @staticmethod
    def get_pk(event: Event):
        return event.group_name

    @staticmethod
    def get_label(event: Event):
        date_str = event.date.strftime('%d.%m.%Y')
        return f"{event.event_name} | {date_str} | {event.group_name}"
