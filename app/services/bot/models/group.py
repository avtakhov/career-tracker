import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.core.db.base import Base
from app.services.bot.models import User


class Group(Base):
    __tablename__ = "groups"

    group_name = sqla.Column(sqla.String, nullable=False, primary_key=True)
    users = relationship("User", secondary="users_groups", viewonly=True)

    def __str__(self):
        return self.group_name
