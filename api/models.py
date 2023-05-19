from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenModel(BaseModel):
    profile_uuid: UUID
    created_at: datetime
    expires_in: datetime
