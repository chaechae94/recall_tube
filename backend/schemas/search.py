from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class SearchResultRead(BaseModel):
    video_id: int
    video_title: str
    start_time: float
    end_time: float
    speech_text: str
    ocr_text: str
    score: float
