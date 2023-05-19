from uuid import UUID

from pydantic import BaseModel

from app.models.user import UserModel


class RecordModel(BaseModel):
    uuid: UUID
    user: UserModel

    class Config:
        orm_mode = True
