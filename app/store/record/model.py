import uuid

from sqlalchemy import Column, UUID, ForeignKey

from app.store.database import BASE


class RecordModelDB(BASE):
    __tablename__ = "record"

    uuid = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)
    user = Column(UUID, ForeignKey("user.uuid", ondelete="CASCADE"), nullable=False)
