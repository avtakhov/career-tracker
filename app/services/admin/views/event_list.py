import sqlalchemy as sqla

from app.core.db.base import sync_session
from app.services.bot.models import Event


class EventList:
    @staticmethod
    def get_events():
        with sync_session() as session:
            result = session.execute(
                sqla.select(Event)
            )
            return result.scalars().all()

    @staticmethod
    def get_pk(event: Event):
        return event.event_id

    @staticmethod
    def get_label(event: Event):
        return f"{event.event_name} | {event.date.strftime('%d.%m.%Y')} | {event.group_name}"
