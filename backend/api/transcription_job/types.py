from pydantic import BaseModel

class TranscriptionJob(BaseModel):
    podcast_id: str
    episode_number: str