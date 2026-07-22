from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ai.ocr import extract_text_from_video
from models.ocr_result import OcrResult
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


def run_ocr(db: Session, user: User, video_id: int) -> list[OcrResult]:
    video = _get_owned_video(db, user, video_id)

    detections = extract_text_from_video(video.file_path)

    db.query(OcrResult).filter(OcrResult.video_id == video.id).delete()
    records = [
        OcrResult(video_id=video.id, time=detection["time"], text=detection["text"])
        for detection in detections
    ]
    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records


def get_ocr_results(db: Session, user: User, video_id: int) -> list[OcrResult]:
    video = _get_owned_video(db, user, video_id)
    return (
        db.query(OcrResult)
        .filter(OcrResult.video_id == video.id)
        .order_by(OcrResult.time)
        .all()
    )
