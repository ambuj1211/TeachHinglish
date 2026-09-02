from pydantic import SecretStr

from teachhinglish.core.settings import Settings
from teachhinglish.providers.gemini_key_resolver import GeminiKeyResolver


def test_subject_key_is_preferred():
    settings = Settings(
        _env_file=None,
        gemini_api_physics_key=SecretStr("physics-key"),
        gemini_api_teachhinglish_key=SecretStr("fallback-key"),
    )

    resolver = GeminiKeyResolver(settings)

    assert resolver.resolve("physics") == "physics-key"


def test_fallback_key_is_used():
    settings = Settings(
        _env_file=None,
        gemini_api_teachhinglish_key=SecretStr("fallback-key"),
    )

    resolver = GeminiKeyResolver(settings)

    assert resolver.resolve("physics") == "fallback-key"


def test_missing_subject_uses_fallback():
    settings = Settings(
        _env_file=None,
        gemini_api_teachhinglish_key=SecretStr("fallback-key"),
    )

    resolver = GeminiKeyResolver(settings)

    assert resolver.resolve("new_subject") == "fallback-key"


def test_no_key_returns_none():
    settings = Settings(_env_file=None)

    resolver = GeminiKeyResolver(settings)

    assert resolver.resolve("physics") is None