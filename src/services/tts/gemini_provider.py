import wave
from pathlib import Path

from google import genai
from google.genai import types

from src.core.config import GEMINI_API_KEY
from src.services.tts.base import TTSProvider

DEFAULT_MODEL = "gemini-3.1-flash-tts-preview"
DEFAULT_VOICE = "Kore"

# Gemini TTS returns raw PCM audio at these settings.
SAMPLE_RATE = 24000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit audio


class GeminiTTSProvider(TTSProvider):
    """Text-to-speech using Google's Gemini native TTS models."""

    def __init__(self, voice: str = DEFAULT_VOICE, model: str = DEFAULT_MODEL):
        self.voice = voice
        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_speech(self, text: str, output_path: Path) -> Path | None:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=self.voice,
                            )
                        )
                    ),
                ),
            )

            pcm_data = response.candidates[0].content.parts[0].inline_data.data

            output_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_wave(output_path, pcm_data)

            return output_path

        except Exception as e:
            print(f"[ERROR] Gemini TTS failed to generate speech: {e}")
            return None

    def _save_wave(self, path: Path, pcm_data: bytes) -> None:
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(SAMPLE_WIDTH)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(pcm_data)