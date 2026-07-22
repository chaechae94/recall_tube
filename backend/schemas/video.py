from datetime import datetime

from pydantic import BaseModel


class VideoRead(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True
