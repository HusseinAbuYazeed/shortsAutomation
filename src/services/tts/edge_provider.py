import asyncio
from pathlib import Path

import edge_tts

from src.services.tts.base import TTSProvider

# A natural-sounding English voice. Full list: `edge-tts --list-voices`
DEFAULT_VOICE = "en-US-GuyNeural"


class EdgeTTSProvider(TTSProvider):
    """Free, local text-to-speech using Microsoft's edge-tts."""

    def __init__(self, voice: str = DEFAULT_VOICE):
        self.voice = voice

    def generate_speech(self, text: str, output_path: Path) -> Path | None:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            asyncio.run(self._synthesize(text, output_path))
            return output_path

        except Exception as e:
            print(f"[ERROR] edge-tts failed to generate speech: {e}")
            return None

    async def _synthesize(self, text: str, output_path: Path) -> None:
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(str(output_path))