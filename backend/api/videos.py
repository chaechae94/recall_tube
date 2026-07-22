from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from db.session import get_db
from models.user import User
from schemas.video import VideoRead
from services.video_service import list_videos, save_video

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/upload", response_model=VideoRead, status_code=201)
def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return save_video(db, current_user, file)


@router.get("", response_model=list[VideoRead])
def get_my_videos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_videos(db, current_user)
