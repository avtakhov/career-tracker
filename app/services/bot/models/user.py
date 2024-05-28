import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.core.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = sqla.Column(sqla.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    full_name = sqla.Column(sqla.String, nullable=False)
    amount = sqla.Column(sqla.BigInteger(), nullable=False, default=0)
    telegram_username = sqla.Column(sqla.String, nullable=False)

    groups = relationship("Group", secondary="users_groups", viewonly=True)

    __table_args__ = (
        sqla.CheckConstraint('amount >= 0', name='amount_positive_check'),
        sqla.UniqueConstraint(telegram_username, name='unique_telegram_username')
    )

    def __str__(self):
        return self.full_name
