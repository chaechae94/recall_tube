from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.memory_chunk import MemoryChunk
from models.ocr_result import OcrResult
from models.scene import Scene
from models.transcript_segment import TranscriptSegment
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


def build_memory_chunks(db: Session, user: User, video_id: int) -> list[MemoryChunk]:
    video = _get_owned_video(db, user, video_id)

    scenes = (
        db.query(Scene)
        .filter(Scene.video_id == video.id)
        .order_by(Scene.start_time)
        .all()
    )
    if not scenes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Run scene detection before generating memory chunks",
        )

    transcript_segments = (
        db.query(TranscriptSegment).filter(TranscriptSegment.video_id == video.id).all()
    )
    ocr_results = db.query(OcrResult).filter(OcrResult.video_id == video.id).all()

    db.query(MemoryChunk).filter(MemoryChunk.video_id == video.id).delete()

    records = []
    for scene in scenes:
        speech_text = " ".join(
            segment.text
            for segment in transcript_segments
            if segment.start_time < scene.end_time and segment.end_time > scene.start_time
        )
        ocr_texts = list(
            dict.fromkeys(
                result.text
                for result in ocr_results
                if scene.start_time <= result.time < scene.end_time
            )
        )
        records.append(
            MemoryChunk(
                video_id=video.id,
                start_time=scene.start_time,
                end_time=scene.end_time,
                speech_text=speech_text,
                ocr_text=" ".join(ocr_texts),
            )
        )

    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records


def get_memory_chunks(db: Session, user: User, video_id: int) -> list[MemoryChunk]:
    video = _get_owned_video(db, user, video_id)
    return (
        db.query(MemoryChunk)
        .filter(MemoryChunk.video_id == video.id)
        .order_by(MemoryChunk.start_time)
        .all()
    )
