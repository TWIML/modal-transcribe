from fastapi import APIRouter, HTTPException

from backend.api.utils import debug_logger
from backend.api.diarised_transcribe.types import DiarisedTranscriptionJob

from typing import List
from backend.src.diarised_transcribe.types import FinalTranscriptionObject
from backend.ops.diarised_transcribe.operators import DiariseAndTranscribeModalOperator

from backend import _utils; logger = _utils.get_logger(__name__)

#########################################################################################

DIARISED_TRANSCRIBE_ROUTER = APIRouter(
    responses={404: {"description": "Not found"}},
)

#########################################################################################

@DIARISED_TRANSCRIBE_ROUTER.post("/api/diarised_transcribe")
async def diarised_transcribe_job(params: DiarisedTranscriptionJob):
    final_transcription: FinalTranscriptionObject = DiariseAndTranscribeModalOperator \
    .trigger_process.remote(
        params.podcast_id, 
        params.episode_number,
        params.overwrite_download,
        params.overwrite_diarisation,
        params.overwrite_transcription
    )
    return {'result': final_transcription}