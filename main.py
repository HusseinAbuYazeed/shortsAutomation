import json
import uuid

from fastapi import FastAPI

from src.core.paths import (
    ensure_job_dir,
    script_path,
    voice_path,
)
from src.models.schemas import StoryRequest
from src.services.story_service import process_story
from src.services.tts.factory import get_tts_provider

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Short Maker API is running!"}


@app.post("/generate")
def generate_short(request: StoryRequest):
    job_id = str(uuid.uuid4())
    ensure_job_dir(job_id)

    # Step 1: analysis + structure + script (single Gemini call)
    story_result = process_story(request.story_text)

    if story_result is None:
        return {"error": "Failed to process the story. Check server logs."}

    # Save the script data to this job's folder.
    with open(script_path(job_id), "w", encoding="utf-8") as f:
        json.dump(story_result, f, indent=4, ensure_ascii=False)

    script = story_result["final_script"]

    # Step 2: voiceover using the chosen provider
    try:
        provider = get_tts_provider(request.tts_provider)
    except ValueError as e:
        return {"error": str(e)}

    result_path = provider.generate_speech(script, voice_path(job_id))

    if result_path is None:
        return {"error": "Failed to generate voiceover. Check server logs."}

    return {
        "job_id": job_id,
        "analysis": story_result["analysis"],
        "structure": story_result["structure"],
        "final_script": script,
        "audio_path": str(result_path),
    }