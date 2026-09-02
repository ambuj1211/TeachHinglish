from unittest.mock import Mock, patch

from pydantic import SecretStr
import pytest

from teachhinglish.core.models import Subject

from teachhinglish.core.settings import Settings
from teachhinglish.providers.gemini import GeminiProvider
from teachhinglish.providers.gemini_key_resolver import GeminiKeyResolver


@pytest.mark.asyncio
async def test_gemini_provider_generates_text():
    settings = Settings(
        _env_file=None,
        gemini_api_physics_key=SecretStr("fake-key"),
    )

    resolver = GeminiKeyResolver(settings)
    provider = GeminiProvider(settings, resolver)

    mock_response = Mock()
    mock_response.text = "Newton ka Second Law simple way mein samjho."

    with patch(
        "teachhinglish.providers.gemini.genai.Client"
    ) as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.models.generate_content.return_value = mock_response

        result = await provider.generate(
            "Explain Newton's Second Law.",
            subject=Subject.PHYSICS,
        )

    assert result == "Newton ka Second Law simple way mein samjho."

    mock_client.models.generate_content.assert_called_once_with(
        model="gemini-3.6-flash",
        contents="Explain Newton's Second Law.",
    )

    mock_client_class.assert_called_once_with(api_key="fake-key")
