from pydantic import BaseModel


class EmbeddingStatusRead(BaseModel):
    chunk_id: int
    start_time: float
    end_time: float
    embedding_dim: int
