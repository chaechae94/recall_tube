from pydantic import BaseModel


class MemoryChunkRead(BaseModel):
    id: int
    start_time: float
    end_time: float
    speech_text: str
    ocr_text: str

    class Config:
        from_attributes = True
