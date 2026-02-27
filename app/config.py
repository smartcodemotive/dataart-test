from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:ahsus@localhost:5432/dataart"
    # Default: SQLite for local dev (no Docker). Override with DATABASE_URL when using docker-compose.
    # database_url: str = "sqlite+aiosqlite:///./local.db"

    class Config:
        env_file = ".env"


settings = Settings()
