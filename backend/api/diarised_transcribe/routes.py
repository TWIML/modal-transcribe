from fastapi import APIRouter, HTTPException

from backend.api.utils import debug_logger
from backend.api.diarised_transcribe.types import DiarisedTranscriptionJob

from typing import List
from backend.src.diarised_transcribe.types import CompletedTranscriptObject
from backend.ops.diarised_transcribe.operators import DiariseAndTranscribeModalOperator

from backend import _utils; logger = _utils.get_logger(__name__)

#########################################################################################

DIARISATION_ROUTER = APIRouter(
    responses={404: {"description": "Not found"}},
)

#########################################################################################

@DIARISATION_ROUTER.post("/api/diarised_transcribe")
async def diarised_transcribe_job(params: DiarisedTranscriptionJob):
    diarised_transcriptions: CompletedTranscriptObject = DiariseAndTranscribeModalOperator \
    .trigger_process.remote(
        params.podcast_id, 
        params.episode_number, 
        params.hf_access_token
    )
    return {'result': diarised_transcriptions}