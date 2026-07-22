import os
from functools import lru_cache

import whisper

from app.core.config import settings

if settings.ffmpeg_dir:
    os.environ["PATH"] = settings.ffmpeg_dir + os.pathsep + os.environ["PATH"]


@lru_cache(maxsize=1)
def _get_model():
    return whisper.load_model(settings.whisper_model_size)


def transcribe(file_path: str) -> list[dict]:
    model = _get_model()
    result = model.transcribe(file_path)
    return [
        {"start": seg["start"], "end": seg["end"], "text": seg["text"].strip()}
        for seg in result["segments"]
    ]
