from pydantic import BaseModel

class DiarisedTranscriptionJob(BaseModel):
    podcast_id: str
    episode_number: str
    hf_access_token: str
    overwrite_download: bool
    overwrite_diarisation: bool
    overwrite_transcription: bool