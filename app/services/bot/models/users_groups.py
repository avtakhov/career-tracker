import sqlalchemy as sqla

from app.core.db.base import Base


class UsersGroups(Base):
    __tablename__ = "users_groups"

    user_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey("users.user_id", ondelete="cascade"), nullable=False, primary_key=True)
    group_name = sqla.Column(sqla.String, sqla.ForeignKey("groups.group_name", ondelete="cascade"), nullable=False, primary_key=True)
