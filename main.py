import uuid
from pathlib import Path

from fastapi import FastAPI

from src.models.schemas import StoryRequest
from src.services.story_service import process_story
from src.services.tts.factory import get_tts_provider

app = FastAPI()

OUTPUT_DIR = Path("outputs")


@app.get("/")
def read_root():
    return {"message": "Short Maker API is running!"}


@app.post("/generate")
def generate_short(request: StoryRequest):
    # Step 1: analysis + structure + script (single Gemini call)
    story_result = process_story(request.story_text)

    if story_result is None:
        return {"error": "Failed to process the story. Check server logs."}

    script = story_result["final_script"]

    # Step 2: voiceover using the chosen provider
    try:
        provider = get_tts_provider(request.tts_provider)
    except ValueError as e:
        return {"error": str(e)}

    job_id = str(uuid.uuid4())
    audio_filename = f"{job_id}.wav" if request.tts_provider == "gemini" else f"{job_id}.mp3"
    audio_path = OUTPUT_DIR / audio_filename

    result_path = provider.generate_speech(script, audio_path)

    if result_path is None:
        return {"error": "Failed to generate voiceover. Check server logs."}

    return {
        "job_id": job_id,
        "analysis": story_result["analysis"],
        "structure": story_result["structure"],
        "final_script": script,
        "audio_path": str(result_path),
    }