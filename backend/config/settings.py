"""
Application configuration settings.
Loads configuration from environment variables with sensible defaults.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    app_name: str = "ClashFish"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "production"

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_port: int = 3000

    # Clash Royale API
    clash_royale_api_key: str = ""
    clash_royale_api_url: str = "https://api.clashroyale.com/v1"
    use_mock_data: bool = True  # Default to mock data

    # Database
    database_url: str = "postgresql://clashfish:clashfish@localhost:5432/clashfish"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl: int = 3600

    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "clashfish"

    # AI/LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-4-5-20251101"

    # ML Models
    ml_model_path: str = "./ml/models"
    win_prob_model_version: str = "v1.0"
    move_eval_model_version: str = "v1.0"

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Security
    secret_key: str = "change_this_to_a_random_secret_key"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    # Monitoring
    sentry_dsn: str = ""
    enable_prometheus: bool = True

    # Computed properties
    @property
    def api_available(self) -> bool:
        """Check if Clash Royale API is configured."""
        return bool(self.clash_royale_api_key) and not self.use_mock_data

    @property
    def llm_available(self) -> bool:
        """Check if any LLM service is configured."""
        return bool(self.openai_api_key or self.anthropic_api_key)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    This is cached so we only load environment variables once.
    """
    return Settings()


# Convenience instance for importing
settings = get_settings()
