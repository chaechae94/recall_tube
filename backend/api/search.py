from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from db.session import get_db
from models.user import User
from schemas.search import SearchRequest, SearchResultRead
from services.search_service import search_memory

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=list[SearchResultRead])
def search(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_memory(db, current_user, request.query, request.limit)
