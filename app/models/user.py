from uuid import UUID

from pydantic import BaseModel


class UserModel(BaseModel):
    uuid: UUID
    name: str

    class Config:
        orm_mode = True
