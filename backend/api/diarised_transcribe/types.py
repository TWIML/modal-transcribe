from pydantic import BaseModel

class DiarisedTranscriptionJob(BaseModel):
    podcast_id: str
    episode_number: str
    hf_access_token: str