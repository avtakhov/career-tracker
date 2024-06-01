import sqlalchemy as sqla

from app.core.db.base import sync_session
from app.services.bot.models import Group


class GroupList:
    @staticmethod
    def get():
        with sync_session() as session:
            result = session.execute(
                sqla.select(Group)
            )
            return result.scalars().all()

    @staticmethod
    def get_pk(group: Group):
        return group.group_name

    @staticmethod
    def get_label(group: Group):
        return group.group_name
