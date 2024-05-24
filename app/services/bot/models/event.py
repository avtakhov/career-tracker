import sqlalchemy as sqla

from app.core.db.base import Base


class Event(Base):
    __tablename__ = "events"

    event_id = sqla.Column(sqla.BigInteger, nullable=False, primary_key=True)
    event_name = sqla.Column(sqla.String, nullable=False)
    description = sqla.Column(sqla.String, nullable=False)
    date = sqla.Column(sqla.Date, nullable=False)
    group_name = sqla.Column(sqla.String, sqla.ForeignKey('groups.group_name', ondelete="cascade"), nullable=False)

    __table_args__ = (
        sqla.Index('date_index', 'date'),
    )
