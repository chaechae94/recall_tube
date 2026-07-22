from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ai.embedding import embed_texts
from models.memory_chunk import MemoryChunk
from models.user import User
from models.video import Video


def _get_owned_video(db: Session, user: User, video_id: int) -> Video:
    video = (
        db.query(Video).filter(Video.id == video_id, Video.owner_id == user.id).first()
    )
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    return video


def _get_chunks(db: Session, video: Video) -> list[MemoryChunk]:
    chunks = (
        db.query(MemoryChunk)
        .filter(MemoryChunk.video_id == video.id)
        .order_by(MemoryChunk.start_time)
        .all()
    )
    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Generate memory chunks before creating embeddings",
        )
    return chunks


def run_embedding(db: Session, user: User, video_id: int) -> list[MemoryChunk]:
    video = _get_owned_video(db, user, video_id)
    chunks = _get_chunks(db, video)

    texts = [f"{chunk.speech_text} {chunk.ocr_text}".strip() for chunk in chunks]
    vectors = embed_texts(texts)

    for chunk, vector in zip(chunks, vectors):
        chunk.embedding = vector
    db.commit()
    for chunk in chunks:
        db.refresh(chunk)
    return chunks


def get_embedding_status(db: Session, user: User, video_id: int) -> list[MemoryChunk]:
    video = _get_owned_video(db, user, video_id)
    return _get_chunks(db, video)
