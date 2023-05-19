from uuid import UUID

from app.exceptions.database_exceptions import NotFound
from app.managers._base import BaseManager
from app.models import RecordModel


class RecordManager(BaseManager):
    async def check_existing(self, *, uuid: UUID):
        try:
            await self.app.store.record_accessor.get(uuid=uuid)
        except NotFound:
            return False
        return True

    async def get(self, *, uuid: UUID) -> RecordModel:
        record = await self.app.store.record_accessor.get(uuid=uuid)
        record.user = await self.app.managers.user_manager.get(uuid=record.user)
        return RecordModel.from_orm(record)

    async def create(self, *, user: UUID) -> RecordModel:
        record = await self.app.store.record_accessor.create(user=user)
        return await self.get(uuid=record.uuid)
