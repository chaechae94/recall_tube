from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Memory Search API"
    database_url: str = "postgresql+psycopg://recalltube:recalltube@localhost:5432/recalltube"
    # 개발용 기본값. 배포 전 반드시 .env의 JWT_SECRET_KEY를 임의의 긴 값으로 교체할 것.
    jwt_secret_key: str = "dev-only-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    upload_dir: str = "uploads"
    whisper_model_size: str = "base"
    # 시스템 PATH에 ffmpeg이 없을 때만 사용. 비어있으면 PATH의 ffmpeg을 그대로 사용.
    ffmpeg_dir: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
