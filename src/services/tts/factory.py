from src.services.tts.base import TTSProvider
from src.services.tts.edge_provider import EdgeTTSProvider
from src.services.tts.gemini_provider import GeminiTTSProvider

# Registry of available providers. Add new ones here as they're built
# (e.g. "elevenlabs": ElevenLabsProvider).
_PROVIDERS = {
    "edge": EdgeTTSProvider,
    "gemini": GeminiTTSProvider,
}

DEFAULT_PROVIDER = "edge"  # free, so it's the safe default for quota


def get_tts_provider(name: str = DEFAULT_PROVIDER) -> TTSProvider:
    """
    Return an instance of the requested TTS provider.

    Raises ValueError if the provider name is not recognized, so
    invalid input fails loudly instead of silently doing the wrong thing.
    """
    provider_class = _PROVIDERS.get(name)

    if provider_class is None:
        available = ", ".join(_PROVIDERS.keys())
        raise ValueError(
            f"Unknown TTS provider '{name}'. Available options: {available}"
        )

    return provider_class()