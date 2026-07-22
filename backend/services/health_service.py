from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings


def get_health_status():
    return {"status": "ok", "app": settings.app_name}


def get_db_health(db: Session):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
