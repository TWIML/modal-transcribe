import time
from typing import List, Union, Tuple
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException

from backend.api.utils import debug_logger
from backend.api.diarised_transcribe.types import DiarisedTranscriptionJob

from backend.ops.types import InProgressJob
from backend.ops.stub import stub

from backend.ops.diarised_transcribe.operators import DiariseAndTranscribeModalOperator
from backend.ops.transcription_job.constants import MAX_JOB_AGE_SECS

from backend.src.diarised_transcribe.types import DiarisationResult

from backend.ops import storage

from backend import _utils; logger = _utils.get_logger(__name__)

#########################################################################################

DIARISATION_ROUTER = APIRouter(
    responses={404: {"description": "Not found"}},
)

#########################################################################################

@DIARISATION_ROUTER.get('/api/diarised_transcribe/diarisation_step')
async def diarisation_step(params: DiarisedTranscriptionJob) -> Union[None, Tuple[DiarisationResult, str]]:

    diarisation_result: Union[
        DiarisationResult,
        None
     ] = DiariseAndTranscribeModalOperator.trigger_diarisation.remote(
        params.podcast_id, 
        params.episode_number, 
        params.hf_access_token
    )
    
    if diarisation_result:
        diarisation_json = diarisation_result.model_dump_json()
        logger.info(
            diarisation_json
        )
        return  diarisation_result, diarisation_json # {'response': result_json}
    else:
        raise HTTPException(
            500,
            detail=f"""
            We have experienced an error in trying to diarise the audio for:
                episode_number: `{params.episode_number}`,
                for the `{params.podcast_id}`

            Have you made certain the credentials for any api's you entered are
            correct eg. for the Hugging Face platform
            """
        )

@DIARISATION_ROUTER.post("/api/diarised_transcribe")
async def diarised_transcribe_job(params: DiarisedTranscriptionJob):
    response = await diarisation_step(params=params)
    if response:
        diarisation_result, diarisation_json = response
        return {'response': diarisation_json}
    
    # NOTE: need to pass whisper model_name in for the call (do you need to init, do you need a singleton?)
