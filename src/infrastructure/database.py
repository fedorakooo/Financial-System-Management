from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
)

from src.infrastructure.config import settings

DATABASE_URL = settings.db.url

async_engine = create_async_engine(DATABASE_URL, echo=settings.db.echo)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=True)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        else:
            await db.commit()
