from teachhinglish.core.settings import Settings


class GeminiKeyResolver:
    """Resolves the Gemini API key for a subject."""

    _SUBJECT_TO_SETTING = {
        "physics": "gemini_api_physics_key",
        "mathematics": "gemini_api_mathematics_key",
        "chemistry": "gemini_api_chemistry_key",
        "biology": "gemini_api_biology_key",
        "history": "gemini_api_history_key",
        "civics": "gemini_api_civics_key",
        "geography": "gemini_api_geography_key",
        "english_grammar": "gemini_api_english_grammar_key",
        "computer_science": "gemini_api_computer_science_key",
        "engineering_mathematics": "gemini_api_engineering_mathematics_key",
        "digital_logic": "gemini_api_digital_logic_key",
        "general": "gemini_api_general_key",
    }

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def resolve(self, subject: str) -> str | None:
        """Return subject-specific key, falling back to TeachHinglish key."""

        setting_name = self._SUBJECT_TO_SETTING.get(subject)

        if setting_name is not None:
            subject_key = getattr(self.settings, setting_name)

            if subject_key is not None:
                value = subject_key.get_secret_value().strip()

                if value:
                    return value

        fallback = self.settings.gemini_api_teachhinglish_key

        if fallback is not None:
            value = fallback.get_secret_value().strip()

            if value:
                return value

        return None
