import time
from typing import List
from fastapi import APIRouter, Request, BackgroundTasks

from backend.api.utils import debug_logger
from backend.api.transcription_job.types import TranscriptionJob

from backend.ops.types import InProgressJob
from backend.ops.stub import stub

from backend.ops.transcription_job.operators import process_episode
from backend.ops.transcription_job.constants import MAX_JOB_AGE_SECS

from backend.ops import storage

from backend import _utils; logger = _utils.get_logger(__name__)

#########################################################################################

TRANSCRIPTION_ROUTER = APIRouter(
    responses={404: {"description": "Not found"}},
)

#########################################################################################

@TRANSCRIPTION_ROUTER.post("/api/transcription_job")
async def transcribe_job(params: TranscriptionJob):
    debug_logger()
    now = int(time.time())
    try:
        inprogress_job = stub.in_progress[params.episode_number]
        # NB: runtime type check is to handle present of old `str` values that didn't expire.
        if (
            isinstance(inprogress_job, InProgressJob)
            and (now - inprogress_job.start_time) < MAX_JOB_AGE_SECS
        ):
            existing_call_id = inprogress_job.call_id
            logger.info(
                f"Found existing, unexpired call ID {existing_call_id} for episode {params.episode_number}"
            )
            return {"call_id": existing_call_id}
    except KeyError:
        pass

    job = process_episode.spawn(params.podcast_id, params.episode_number)
    stub.in_progress[params.episode_number] = InProgressJob(
        job_id=job.object_id, start_time=now
    )

    return {"job_id": job.object_id}


@TRANSCRIPTION_ROUTER.get("/api/transcription_job/{call_id}")
async def poll_status(call_id: str):
    from modal.call_graph import InputInfo, InputStatus
    from modal.functions import FunctionCall

    debug_logger()
    
    function_call = FunctionCall.from_id(call_id)
    graph: List[InputInfo] = function_call.get_call_graph()

    try:
        function_call.get(timeout=0.1)
    except TimeoutError:
        pass
    except Exception as exc:
        if exc.args:
            inner_exc = exc.args[0]
            if "HTTPError 403" in inner_exc:
                return dict(error="permission denied on podcast audio download")
        return dict(error="unknown job processing error")

    try:
        map_root = graph[0].children[0].children[0]
    except IndexError:
        return dict(finished=False)

    assert map_root.function_name == "transcribe_episode"

    leaves = map_root.children
    tasks = len(set([leaf.task_id for leaf in leaves]))
    done_segments = len(
        [leaf for leaf in leaves if leaf.status == InputStatus.SUCCESS]
    )
    total_segments = len(leaves)
    finished = map_root.status == InputStatus.SUCCESS

    return dict(
        finished=finished,
        total_segments=total_segments,
        tasks=tasks,
        done_segments=done_segments,
    )


##########################################################
# NOTE: 13/02/2024, Vishnu - 
# Working in a separate section in the api.py file as it
# does not seem like (modal? fastapi?) it likes hosting
# the @web_app.get/post decorator in alternative files
# and so I can not build routes there. Also routes are
# all I can work with now as the html/svelte side of 
# things is playing up and I don't understand it enoug
# to troubleshoot just yet, same for bruno etc. so just
# focussing on modal and fastapi side of things for now
##########################################################

@TRANSCRIPTION_ROUTER.get("/api2")
async def api2_root(request: Request):
    msg = 'Welcome to the 2nd API route'
    return msg


# a function for triggering the downloading, transcribing and annotating of a fixed url podcast on a single proces
@TRANSCRIPTION_ROUTER.get("/api2/trigger_process")
async def trigger_process(bgd_tasks: BackgroundTasks):
    fixed_podcast_url = "https://chrt.fm/track/4D4ED/traffic.megaphone.fm/MLN7496446704.mp3?updated=1707160554"
    from backend.ops.transcription_job.operators import download_transcribe_annotate_fixed_podcast_in_single_job_process

    (
        download_step_msgs,
        transcript_storage_location_msg,
        transcription_text
    ) = download_transcribe_annotate_fixed_podcast_in_single_job_process.remote(fixed_podcast_url)

    ''' # cant get return from bgd task, must write and read
    bgd_tasks.add_task(
        func=download_transcribe_annotate_fixed_podcast_in_single_job_process.remote,
        fixed_podcast_url=fixed_podcast_url
    )'''

    return {
        'fixed_podcast_url': fixed_podcast_url,
        'size_msg': download_step_msgs['size_msg'],
        'audio_stored_msg': download_step_msgs['audio_stored_msg'],
        'transcript_stored_msg': transcript_storage_location_msg,
        'transcription_text': transcription_text
    }