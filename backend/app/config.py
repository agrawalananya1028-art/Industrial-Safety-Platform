"""Application Configuration"""

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/safety_db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 300

    # OpenAI/LLM
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"
    OPENAI_TEMPERATURE: float = 0.7

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # Data Generation
    SENSOR_UPDATE_INTERVAL: int = 3
    MOCK_DATA_GENERATION_ENABLED: bool = True
    INCIDENT_SIMULATION_ENABLED: bool = True

    # Notifications
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    ALERT_EMAIL_RECIPIENT: str = "safety@company.com"

    # SMS
    SMS_PROVIDER: str = "twilio"
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # Slack
    SLACK_WEBHOOK_URL: str = ""
    SLACK_CHANNEL: str = "safety-alerts"

    # RAG
    FAISS_INDEX_PATH: str = "./data/faiss_index"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    SIMILARITY_THRESHOLD: float = 0.7

    # Feature Flags
    FEATURE_VOICE_ALERTS: bool = False
    FEATURE_DIGITAL_TWIN: bool = False
    FEATURE_PREDICTIVE_ALERTS: bool = True
    FEATURE_SMS_ALERTS: bool = False
    FEATURE_EMAIL_ALERTS: bool = True

    # Compliance
    OISD_COMPLIANCE_MODE: bool = True
    DGMS_COMPLIANCE_MODE: bool = True
    FACTORY_ACT_COMPLIANCE_MODE: bool = True

    # Performance
    WORKER_THREADS: int = 4
    API_REQUEST_TIMEOUT: int = 60

    # Timezone
    TIMEZONE: str = "Asia/Kolkata"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse allowed origins from comma-separated string"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)"""
    return Settings()
