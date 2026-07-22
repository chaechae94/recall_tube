from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ai.stt import transcribe
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


def transcribe_video(db: Session, user: User, video_id: int) -> list[TranscriptSegment]:
    video = _get_owned_video(db, user, video_id)

    segments = transcribe(video.file_path)

    db.query(TranscriptSegment).filter(TranscriptSegment.video_id == video.id).delete()
    records = [
        TranscriptSegment(
            video_id=video.id,
            start_time=segment["start"],
            end_time=segment["end"],
            text=segment["text"],
        )
        for segment in segments
    ]
    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records


def get_transcript(db: Session, user: User, video_id: int) -> list[TranscriptSegment]:
    video = _get_owned_video(db, user, video_id)
    return (
        db.query(TranscriptSegment)
        .filter(TranscriptSegment.video_id == video.id)
        .order_by(TranscriptSegment.start_time)
        .all()
    )
