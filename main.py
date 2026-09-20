from fastapi import FastAPI

from src.models.schemas import StoryRequest
from src.services.story_service import process_story

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Short Maker API is running!"}


@app.post("/generate")
def generate_short(request: StoryRequest):
    result = process_story(request.story_text)

    if result is None:
        return {"error": "Failed to process the story. Check server logs."}

    return result