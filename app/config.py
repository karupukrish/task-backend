from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql://postgres:root@localhost:5432/project_mgmt",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )
    jwt_secret: str = Field(
        default="super-secret-key-change-in-production",
        validation_alias=AliasChoices("JWT_SECRET", "jwt_secret"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    jwt_expiry_hours: int = Field(
        default=24,
        validation_alias=AliasChoices("JWT_EXPIRY_HOURS", "jwt_expiry_hours"),
    )
    frontend_url: str = Field(
        default="http://localhost:3000",
        validation_alias=AliasChoices("FRONTEND_URL", "frontend_url"),
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

