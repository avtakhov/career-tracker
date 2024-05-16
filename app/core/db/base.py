from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine

from app.settings import settings

import sqlalchemy as sqla
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


def get_engine(db_url: str = settings.database_url) -> AsyncEngine:
    return create_async_engine(db_url, echo=True)


# noinspection PyTypeChecker
async_session = sessionmaker(
    get_engine(), class_=AsyncSession, expire_on_commit=False
)
