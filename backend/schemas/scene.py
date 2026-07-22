from pydantic import BaseModel


class SceneRead(BaseModel):
    id: int
    start_time: float
    end_time: float

    class Config:
        from_attributes = True
