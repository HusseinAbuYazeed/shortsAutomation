from abc import ABC, abstractmethod
from pathlib import Path


class TTSProvider(ABC):
    """
    Common interface every voiceover provider must implement.

    Whatever provider is chosen (edge-tts, Gemini TTS, ElevenLabs...),
    the rest of the app only ever talks to this interface — it never
    needs to know which provider is actually running underneath.
    """

    @abstractmethod
    def generate_speech(self, text: str, output_path: Path) -> Path | None:
        """
        Convert `text` into a speech audio file saved at `output_path`.

        Returns the path to the generated audio file on success,
        or None if generation failed.
        """
        raise NotImplementedError