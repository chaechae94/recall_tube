import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from models.user import User
from models.video import Video

ALLOWED_CONTENT_TYPES = {"video/mp4"}


def save_video(db: Session, user: User, file: UploadFile) -> Video:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only mp4 uploads are supported",
        )

    user_dir = Path(settings.upload_dir) / str(user.id)
    user_dir.mkdir(parents=True, exist_ok=True)

    dest_path = user_dir / f"{uuid.uuid4()}.mp4"
    with dest_path.open("wb") as out:
        while chunk := file.file.read(1024 * 1024):
            out.write(chunk)

    video = Video(
        owner_id=user.id,
        title=file.filename or dest_path.name,
        file_path=str(dest_path),
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


def list_videos(db: Session, user: User) -> list[Video]:
    return (
        db.query(Video)
        .filter(Video.owner_id == user.id)
        .order_by(Video.created_at.desc())
        .all()
    )
