from pydantic import BaseModel

class StoryRequest(BaseModel):
    story_text: str

class StoryResponse(BaseModel):
    message: str
    job_id: str