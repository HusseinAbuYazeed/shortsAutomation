from pathlib import Path

from src.services.tts.gemini_provider import GeminiTTSProvider

provider = GeminiTTSProvider()

result = provider.generate_speech(
    text="Say cheerfully: This is a test of the Gemini voiceover system.",
    output_path=Path("test_output_gemini.wav"),
)

if result:
    print(f"Success! Audio saved to: {result}")
else:
    print("Failed to generate audio.")