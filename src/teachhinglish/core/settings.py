from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Gemini — subject-specific keys
    gemini_api_physics_key: SecretStr | None = None
    gemini_api_mathematics_key: SecretStr | None = None
    gemini_api_chemistry_key: SecretStr | None = None
    gemini_api_biology_key: SecretStr | None = None
    gemini_api_history_key: SecretStr | None = None
    gemini_api_civics_key: SecretStr | None = None
    gemini_api_geography_key: SecretStr | None = None
    gemini_api_english_grammar_key: SecretStr | None = None
    gemini_api_computer_science_key: SecretStr | None = None
    gemini_api_engineering_mathematics_key: SecretStr | None = None
    gemini_api_digital_logic_key: SecretStr | None = None
    gemini_api_general_key: SecretStr | None = None

    # Gemini fallback
    gemini_api_teachhinglish_key: SecretStr | None = None

    # NVIDIA / Nemotron
    nvidia_api_key: SecretStr | None = None
    nemotron_model: str = "nvidia/nemotron-3-super-120b-a12b"


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
