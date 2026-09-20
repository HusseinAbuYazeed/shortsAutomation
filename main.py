from fastapi import FastAPI
from src.models.schemas import StoryRequest, StoryResponse
import uuid

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Short Maker API is running!"}

@app.post("/generate", response_model=StoryResponse)
def generate_short(request: StoryRequest):
    job_id = str(uuid.uuid4())
    print(f"Received story: {request.story_text[:50]}...")
    
    return StoryResponse(
        message="Story received successfully",
        job_id=job_id
    )