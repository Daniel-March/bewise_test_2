from uuid import UUID

from app.managers._base import BaseManager
from app.models import UserModel


class UserManager(BaseManager):
    async def get(self, *, uuid: UUID) -> UserModel:
        user = await self.app.store.user_accessor.get(uuid=uuid)

        return UserModel.from_orm(user)

    async def create(self, *, name: str) -> UserModel:
        user = await self.app.store.user_accessor.create(name=name)

        return await self.get(uuid=user.uuid)

