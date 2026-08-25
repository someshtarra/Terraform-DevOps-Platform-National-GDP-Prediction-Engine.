import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "National GDP Prediction Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENV: str = os.getenv("APP_ENV", "dev")

    # Host & Port
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 2

    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres_password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "gdp_db")
    DATABASE_URL: Optional[str] = None

    # Redis Cache
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    # S3 Model Storage
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "gdp-prediction-models-dev")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    # Dataset path
    DATASET_PATH: str = os.getenv("DATASET_PATH", "src/data/GDP.csv")

    # Security / CORS
    CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
