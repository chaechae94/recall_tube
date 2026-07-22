from fastapi import FastAPI

from api.auth import router as auth_router
from api.health import router as health_router
from app.core.config import settings
from db.session import Base, engine
from models import user as _user  # noqa: F401  ensure model is registered on Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(auth_router)
