from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from db.session import get_db
from models.user import User
from schemas.search import SearchRequest, SearchResponse
from services.search_service import search_memory

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expanded_query, results = search_memory(
        db, current_user, request.query, request.limit, request.use_expansion
    )
    return SearchResponse(expanded_query=expanded_query, results=results)
