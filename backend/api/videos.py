from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from db.session import get_db
from models.memory_chunk import MemoryChunk
from models.user import User
from schemas.embedding import EmbeddingStatusRead
from schemas.memory_chunk import MemoryChunkRead
from schemas.ocr import OcrResultRead
from schemas.scene import SceneRead
from schemas.transcript import TranscriptSegmentRead
from schemas.video import VideoRead
from services.embedding_service import get_embedding_status, run_embedding
from services.memory_chunk_service import build_memory_chunks, get_memory_chunks
from services.ocr_service import get_ocr_results, run_ocr
from services.scene_service import get_scenes, run_scene_detection
from services.transcription_service import get_transcript, transcribe_video
from services.video_service import list_videos, save_video


def _to_embedding_status(chunk: MemoryChunk) -> EmbeddingStatusRead:
    return EmbeddingStatusRead(
        chunk_id=chunk.id,
        start_time=chunk.start_time,
        end_time=chunk.end_time,
        embedding_dim=len(chunk.embedding) if chunk.embedding is not None else 0,
    )

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


@router.post("/{video_id}/transcribe", response_model=list[TranscriptSegmentRead])
def transcribe(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return transcribe_video(db, current_user, video_id)


@router.get("/{video_id}/transcript", response_model=list[TranscriptSegmentRead])
def read_transcript(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_transcript(db, current_user, video_id)


@router.post("/{video_id}/ocr", response_model=list[OcrResultRead])
def ocr(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return run_ocr(db, current_user, video_id)


@router.get("/{video_id}/ocr", response_model=list[OcrResultRead])
def read_ocr(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_ocr_results(db, current_user, video_id)


@router.post("/{video_id}/scenes", response_model=list[SceneRead])
def scenes(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return run_scene_detection(db, current_user, video_id)


@router.get("/{video_id}/scenes", response_model=list[SceneRead])
def read_scenes(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_scenes(db, current_user, video_id)


@router.post("/{video_id}/memory-chunks", response_model=list[MemoryChunkRead])
def memory_chunks(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return build_memory_chunks(db, current_user, video_id)


@router.get("/{video_id}/memory-chunks", response_model=list[MemoryChunkRead])
def read_memory_chunks(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_memory_chunks(db, current_user, video_id)


@router.post("/{video_id}/embeddings", response_model=list[EmbeddingStatusRead])
def embeddings(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chunks = run_embedding(db, current_user, video_id)
    return [_to_embedding_status(chunk) for chunk in chunks]


@router.get("/{video_id}/embeddings", response_model=list[EmbeddingStatusRead])
def read_embeddings(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chunks = get_embedding_status(db, current_user, video_id)
    return [_to_embedding_status(chunk) for chunk in chunks]
