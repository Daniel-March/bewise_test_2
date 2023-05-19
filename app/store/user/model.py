import uuid

from sqlalchemy import Column, UUID, String

from app.store.database import BASE


class UserModelDB(BASE):
    __tablename__ = "user"

    uuid = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
