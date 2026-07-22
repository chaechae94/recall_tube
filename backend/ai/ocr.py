from functools import lru_cache

import cv2
from paddleocr import PaddleOCR

from app.core.config import settings

MIN_CONFIDENCE = 0.5


@lru_cache(maxsize=1)
def _get_ocr():
    return PaddleOCR(use_angle_cls=True, lang="en")


def extract_text_from_video(file_path: str) -> list[dict]:
    ocr = _get_ocr()
    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_interval = max(int(fps * settings.ocr_frame_interval_seconds), 1)

    results = []
    frame_idx = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_interval == 0:
                timestamp = frame_idx / fps
                lines = ocr.ocr(frame, cls=True)
                texts = [
                    text
                    for line in (lines[0] if lines else [])
                    for _, (text, score) in [line]
                    if score >= MIN_CONFIDENCE
                ]
                if texts:
                    results.append({"time": timestamp, "text": " ".join(texts)})
            frame_idx += 1
    finally:
        cap.release()

    return results
