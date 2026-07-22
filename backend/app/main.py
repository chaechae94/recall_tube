from fastapi import FastAPI
from sqlalchemy import text

from api.auth import router as auth_router
from api.health import router as health_router
from api.search import router as search_router
from api.videos import router as videos_router
from app.core.config import settings
from db.session import Base, engine
from models import memory_chunk as _memory_chunk  # noqa: F401
from models import ocr_result as _ocr_result  # noqa: F401
from models import scene as _scene  # noqa: F401
from models import transcript_segment as _transcript_segment  # noqa: F401
from models import user as _user  # noqa: F401  ensure model is registered on Base
from models import video as _video  # noqa: F401  ensure model is registered on Base

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(videos_router)
app.include_router(search_router)
