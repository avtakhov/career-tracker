import sqlalchemy as sqla

from app.core.db.base import sync_session
from app.services.bot.models import Group


class GroupList:
    @staticmethod
    def get():
        with sync_session() as session:
            result = session.execute(
                sqla.select(Group.group_name)
            )
            return result.scalars().all()

    @staticmethod
    def get_pk(group_name: str):
        return group_name

    @staticmethod
    def get_label(group_name: str):
        return group_name
