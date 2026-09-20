from pydantic import BaseModel


class StoryRequest(BaseModel):
    story_text: str
    tts_provider: str = "edge"  # "edge" | "gemini" | (future: "elevenlabs")
    
class StoryResponse(BaseModel):
    message: str
    job_id: str