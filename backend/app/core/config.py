from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Memory Search API"
    database_url: str = "postgresql+psycopg://recalltube:recalltube@localhost:5432/recalltube"

    class Config:
        env_file = ".env"


settings = Settings()
