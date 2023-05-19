from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

if TYPE_CHECKING:
    from app import App

BASE = declarative_base()


class Database:
    __engine: AsyncEngine

    def __init__(self, app: "App"):
        self.__app = app

    async def connect(self):
        self.__engine = create_async_engine(self.__app.config.database.url)
        async with self.__engine.begin() as conn:
            await conn.run_sync(BASE.metadata.create_all)
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))

    async def disconnect(self):
        await self.__engine.dispose()

    @property
    def make_session(self) -> async_sessionmaker:
        return async_sessionmaker(self.engine, class_=AsyncSession)

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine


async def setup_database(app: "App"):
    app.database = Database(app)
    await app.database.connect()
