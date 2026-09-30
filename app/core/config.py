from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AliasChoices, Field
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str

    # JWT
    jwt_secret_key: str = "change-this-secret-key"
    jwt_algorithm: str = "HS256"

    # Access token
    access_token_expire_minutes: int = 30

    # Refresh token
    refresh_token_expire_days: int = 7

    # Razorpay
    razorpay_key_id: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "RAZORPAY_KEY_ID",
            "API_TEST_KEY",
        ),
    )

    razorpay_key_secret: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "RAZORPAY_KEY_SECRET",
            "API_SECRET_KEY",
            "API_SECRET_KEYS",
        ),
    )

    model_config = SettingsConfigDict(
        env_file=(
            PROJECT_ROOT / ".env",
            PROJECT_ROOT / "app" / ".env",
        ),
        extra="ignore",
    )


settings = Settings()