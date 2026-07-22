from pydantic import BaseModel


class TranscriptSegmentRead(BaseModel):
    id: int
    start_time: float
    end_time: float
    text: str

    class Config:
        from_attributes = True
