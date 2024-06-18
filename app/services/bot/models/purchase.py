import enum

import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from app.core.db.base import Base


class PurchaseStatus(enum.Enum):
    Ordered = "Ordered"
    Received = "Received"
    Cancelled = "Cancelled"


class Purchase(Base):
    __tablename__ = "purchases"

    purchase_id = sqla.Column(sqla.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    product_id = sqla.Column(
        sqla.BigInteger,
        sqla.ForeignKey("products.product_id"),
        nullable=False,
    )
    user_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey("users.user_id", ondelete="cascade"), nullable=False)
    created_at = sqla.Column(sqla.DateTime(timezone=True), nullable=False)
    status = sqla.Column(sqla.Enum(PurchaseStatus), nullable=False, default=PurchaseStatus.Ordered)

    user = relationship("User", viewonly=True)
    product = relationship("Product", viewonly=True)

    __table_args__ = (
        sqla.Index('created_at_index', 'created_at'),
    )
