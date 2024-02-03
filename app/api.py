import asyncio
import json
import time
from tqdm import tqdm
import sys
from typing import List, NamedTuple, Optional

from fastapi import FastAPI, Request

from . import config
from .main import (
    get_podcast_metadata_path,
    get_episode_metadata_path,
    get_transcript_path,
    populate_podcast_metadata,
    process_episode,
    stub,
)
from .podcast import coalesce_short_transcript_segments, the_podcast

from pydantic import BaseModel

logger = config.get_logger(__name__)
web_app = FastAPI()

# A transcription taking > 10 minutes should be exceedingly rare.
MAX_JOB_AGE_SECS = 10 * 60

# The number of episodes to return in the preview
NUM_EPISODES_PREVIEW = 25

# Print verbose logging messages
DEBUG = True

import inspect

class DebugLogger:
    def __init__(self, logger):
        self.logger = logger

    def log(self, level='info', message=None):
        if not DEBUG:
            return
        
        if message is None:
            frame = inspect.stack()[2]
            func_name = frame[3]
            arg_info = inspect.getargvalues(frame[0])
            args = [f"{arg}={arg_info.locals[arg]}" for arg in arg_info.args]
            message = f"*** Entering function: {func_name}, args: {', '.join(args)} ***"

        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)

    def __call__(self, level='info', message=None):
        self.log(level, message)

debug_logger = DebugLogger(logger)


class TranscriptionJob(BaseModel):
    podcast_id: str
    episode_number: str

class InProgressJob(NamedTuple):
    job_id: str
    start_time: int


@web_app.get("/api/podcasts")
async def podcasts_endpoint(request: Request):
    import dataclasses
    debug_logger()
    return [the_podcast]


def sorting_key(item):
    episode_number = item[1].get("episode_number")
    if episode_number is None:
        return (1, 0)
    try:
        # Try to convert the episode number to an integer for sorting
        return (0, int(episode_number))
    except ValueError:
        # If the episode number is a compound number, split it and convert both parts to integers for sorting
        episode, part = map(int, episode_number.split('.'))
        return (0, episode, -part)


@web_app.post("/api/podcast/{podcast_id}")
async def repopulate_metadata(podcast_id: str):
    # Don't run this Modal function in a separate container in the cloud, because then
    # we'd be exposed to a race condition with the NFS if we don't wait for the write
    # to propogate.
    
    debug_logger()

    raw_populate_podcast_metadata = populate_podcast_metadata.get_raw_f()
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None, raw_populate_podcast_metadata, podcast_id
    )


@web_app.get("/api/podcast/{podcast_id}")
async def podcast_endpoint(podcast_id: str):
    debug_logger()

    previously_stored = True

    pod_metadata_path = get_podcast_metadata_path(podcast_id)


    debug_logger(message=f"pod_metadata_path: {pod_metadata_path}")

    if not pod_metadata_path.exists():
        previously_stored = False
        await repopulate_metadata(podcast_id)
        # return dict(error="Podcast metadata not preloaded.")

    ep_metadata_path = get_episode_metadata_path(podcast_id)
    if not ep_metadata_path.exists():
        previously_stored = False
        await repopulate_metadata(podcast_id)
        
    with open(pod_metadata_path, "r") as f:
        pod_metadata = json.load(f)

    episodes = {}

    with open(ep_metadata_path, 'r') as f:
        episodes = json.load(f)

    debug_logger(message=f"Loaded {len(episodes)} episodes.")

    episodes = {k: v for k, v in sorted(episodes.items(), key=sorting_key, reverse=True)}
    
    # Refresh possibly stale data asynchronously.
    if previously_stored:
        populate_podcast_metadata.spawn(podcast_id)

    return dict(pod_metadata=pod_metadata, episodes=episodes)


@web_app.get("/api/podcast/{podcast_id}/episode/{episode_number}")
async def get_episode(podcast_id: str, episode_number: str):
    debug_logger()

    # Load all episodes
    ep_metadata_path = get_episode_metadata_path(podcast_id)
    with open(ep_metadata_path, 'r') as f:
        episodes = json.load(f)

    # Find the episode with the matching number
    episode = episodes[episode_number]
    
    if episode is None:
        return dict(error="Episode not found.")

    episode_guid_hash = episode['guid_hash']

    transcription_path = get_transcript_path(episode_guid_hash)

    if not transcription_path.exists():
        return dict(metadata=episode)

    with open(transcription_path, "r") as f:
        data = json.load(f)

    return dict(
        metadata=episode,
        segments=coalesce_short_transcript_segments(data["segments"]),
    )


@web_app.post("/api/transcription_job")
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


@web_app.get("/api/transcription_job/{call_id}")
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
