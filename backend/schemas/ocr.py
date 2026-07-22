from pydantic import BaseModel


class OcrResultRead(BaseModel):
    id: int
    time: float
    text: str

    class Config:
        from_attributes = True
