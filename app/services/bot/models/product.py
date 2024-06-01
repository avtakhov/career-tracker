import sqlalchemy as sqla

from app.core.db.base import Base


class Product(Base):
    __tablename__ = "products"

    product_id = sqla.Column(sqla.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    name = sqla.Column(sqla.String, nullable=False)
    cost = sqla.Column(sqla.BigInteger, nullable=False)

    __table_args__ = (
        sqla.CheckConstraint('cost >= 0', name='cost_positive_check'),
    )

    def __str__(self):
        return self.name
