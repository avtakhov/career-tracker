import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.core.db.base import Base


class Group(Base):
    __tablename__ = "groups"

    group_name = sqla.Column(sqla.String, nullable=False, primary_key=True)
    users = relationship("User", secondary='users_groups')
