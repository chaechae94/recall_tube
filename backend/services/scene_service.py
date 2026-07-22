from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ai.scene_detection import detect_scenes
from models.scene import Scene
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


def run_scene_detection(db: Session, user: User, video_id: int) -> list[Scene]:
    video = _get_owned_video(db, user, video_id)

    scenes = detect_scenes(video.file_path)

    db.query(Scene).filter(Scene.video_id == video.id).delete()
    records = [
        Scene(video_id=video.id, start_time=scene["start"], end_time=scene["end"])
        for scene in scenes
    ]
    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records


def get_scenes(db: Session, user: User, video_id: int) -> list[Scene]:
    video = _get_owned_video(db, user, video_id)
    return (
        db.query(Scene)
        .filter(Scene.video_id == video.id)
        .order_by(Scene.start_time)
        .all()
    )
