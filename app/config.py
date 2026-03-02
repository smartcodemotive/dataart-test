from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:ahsus@localhost:5432/dataart",
        validation_alias="DATABASE_URL",
    )

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
