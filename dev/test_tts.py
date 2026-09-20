from pathlib import Path

from src.services.tts.edge_provider import EdgeTTSProvider

provider = EdgeTTSProvider()

result = provider.generate_speech(
    text="This is a test of the voiceover system.",
    output_path=Path("test_output.mp3"),
)

if result:
    print(f"Success! Audio saved to: {result}")
else:
    print("Failed to generate audio.")