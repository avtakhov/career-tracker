import sqlalchemy as sqla

from app.core.db.base import Base


class Chat(Base):
    __tablename__ = "chats"
    __table_args__ = (

    )

    telegram_user_id = sqla.Column(sqla.BigInteger, nullable=False, primary_key=True)
    user_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey('users.user_id'), nullable=False)
