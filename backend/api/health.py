from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.health_service import get_db_health, get_health_status

router = APIRouter()


@router.get("/health")
def health():
    return get_health_status()


@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    return get_db_health(db)
