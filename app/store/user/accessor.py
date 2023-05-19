from uuid import UUID

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.exceptions.database_exceptions import NotFound, Conflict
from app.store.base import BaseAccessor
from app.store.user.model import UserModelDB


class UserAccessor(BaseAccessor):
    async def get(self, *, uuid: UUID, make_session: async_sessionmaker = None) -> UserModelDB:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (select(UserModelDB).
                where(UserModelDB.uuid == uuid))

        async with make_session() as session:
            result = await session.scalar(stmt)
            if result is None:
                raise NotFound(text="User not found", data={"uuid": uuid.hex})
            return result

    async def create(self, *, name: str, make_session: async_sessionmaker = None) -> UserModelDB:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (insert(UserModelDB).
                values(name=name))

        async with make_session() as session:
            try:
                inserted_uuid = (await session.execute(stmt)).inserted_primary_key[0]
            except IntegrityError as e:
                raise Conflict(text=f"User creating failed. {e.orig}",
                               data={"name": name})
            await session.commit()
            return await self.get(uuid=inserted_uuid)

    async def update(self, *, uuid: UUID, name: str, make_session: async_sessionmaker = None) -> UserModelDB:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (update(UserModelDB).
                where(UserModelDB.uuid == uuid).
                values(name=name))

        async with make_session() as session:
            try:
                await session.execute(stmt)
            except IntegrityError as e:
                raise Conflict(text=f"User updating failed. {e.orig}",
                               data={"uuid": uuid.hex,
                                     "name": name})
            await session.commit()
            return await self.get(uuid=uuid)

    async def delete(self, *, uuid: UUID, make_session: async_sessionmaker = None) -> None:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (delete(UserModelDB).
                where(UserModelDB.uuid == uuid))

        async with make_session() as session:
            await session.execute(stmt)
            await session.commit()
