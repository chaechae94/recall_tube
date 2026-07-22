from sqlalchemy.orm import Session

from ai.embedding import embed_texts
from models.memory_chunk import MemoryChunk
from models.user import User
from models.video import Video


def search_memory(db: Session, user: User, query: str, limit: int = 10) -> list[dict]:
    query_vector = embed_texts([query])[0]
    distance = MemoryChunk.embedding.cosine_distance(query_vector)

    rows = (
        db.query(MemoryChunk, Video, distance.label("distance"))
        .join(Video, Video.id == MemoryChunk.video_id)
        .filter(Video.owner_id == user.id)
        .filter(MemoryChunk.embedding.is_not(None))
        .order_by(distance)
        .limit(limit)
        .all()
    )

    return [
        {
            "video_id": video.id,
            "video_title": video.title,
            "start_time": chunk.start_time,
            "end_time": chunk.end_time,
            "speech_text": chunk.speech_text,
            "ocr_text": chunk.ocr_text,
            "score": 1 - dist,
        }
        for chunk, video, dist in rows
    ]
