from pydantic import BaseModel

class DiarisationJob(BaseModel):
    podcast_id: str
    episode_number: str
    hf_access_token: str