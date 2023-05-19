from datetime import datetime
from uuid import UUID

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.exceptions.database_exceptions import NotFound, Conflict
from app.store.base import BaseAccessor
from app.store.record.model import RecordModelDB


class RecordAccessor(BaseAccessor):
    async def get(self, *, uuid: UUID, make_session: async_sessionmaker = None) -> RecordModelDB:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (select(RecordModelDB).
                where(RecordModelDB.uuid == uuid))

        async with make_session() as session:
            result = await session.scalar(stmt)
            if result is None:
                raise NotFound(text="Record not found", data={"uuid": uuid.hex})
            return result

    async def create(self, *, user: UUID, make_session: async_sessionmaker = None) -> RecordModelDB:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (insert(RecordModelDB).
                values(user=user))

        async with make_session() as session:
            try:
                inserted_uuid = (await session.execute(stmt)).inserted_primary_key[0]
            except IntegrityError as e:
                raise Conflict(text=f"Record creating failed. {e.orig}",
                               data={"user": user.hex})
            await session.commit()
            return await self.get(uuid=inserted_uuid)

    async def update(self, *, uuid: UUID, user: UUID, make_session: async_sessionmaker = None) -> RecordModelDB:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (update(RecordModelDB).
                where(RecordModelDB.uuid == uuid).
                values(user=user))

        async with make_session() as session:
            try:
                await session.execute(stmt)
            except IntegrityError as e:
                raise Conflict(text=f"Record updating failed. {e.orig}",
                               data={"uuid": uuid.hex,
                                     "user": user.hex})
            await session.commit()
            return await self.get(uuid=uuid)

    async def delete(self, *, uuid: UUID, make_session: async_sessionmaker = None) -> None:
        if make_session is None:
            make_session = self.app.database.make_session

        stmt = (delete(RecordModelDB).
                where(RecordModelDB.uuid == uuid))

        async with make_session() as session:
            await session.execute(stmt)
            await session.commit()
