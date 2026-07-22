# AI Memory Search

영상 시청자를 위한 AI 기억 검색 서비스.

제목이나 태그가 아니라 "곰처럼 생긴 흰 캐릭터", "CNN을 피자로 설명한 영상" 같은
모호한 기억만으로 과거에 본 영상을 다시 찾아준다.

## 구조

```
frontend/    Next.js
backend/     FastAPI (api / services / ai / db / models / schemas / core / utils)
docs/        설계 문서
recalltube/  초기 CRA 프로토타입 (참고용, 별도 관리)
```

## 기술 스택

- Frontend: React, Next.js, TailwindCSS
- Backend: FastAPI (Python)
- DB: PostgreSQL + pgvector
- AI: Whisper, PaddleOCR, OpenCV, PySceneDetect, Qwen2.5-VL, BGE-M3
- Auth: JWT
- Infra: Docker
