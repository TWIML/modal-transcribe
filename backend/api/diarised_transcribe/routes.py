import time
from typing import List, Union
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException

from backend.api.utils import debug_logger
from backend.api.diarised_transcribe.types import DiarisationJob

from backend.ops.types import InProgressJob
from backend.ops.stub import stub

from backend.ops.diarised_transcribe.operators import DiarisationModalOperator
from backend.ops.transcription_job.constants import MAX_JOB_AGE_SECS

from backend.src.diarised_transcribe.types import DiarisationResult

from backend.ops import storage

from backend import _utils; logger = _utils.get_logger(__name__)

#########################################################################################

DIARISATION_ROUTER = APIRouter(
    responses={404: {"description": "Not found"}},
)

#########################################################################################

@DIARISATION_ROUTER.post("/api/diarise_job")
async def diarise_job(params: DiarisationJob):
    
    diarisation_result: Union[
        DiarisationResult,
        None
     ] = DiarisationModalOperator.trigger_diarisation.remote(
        params.podcast_id, 
        params.episode_number, 
        params.hf_access_token
    )

    if diarisation_result:
        result_json = diarisation_result.model_dump_json()
        logger.info(
            result_json
        )
        return {'response': result_json}
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