import asyncio, json
from fastapi import APIRouter, Request, HTTPException

from backend.src.podcast.constants import THE_PODCAST
from backend.src.podcast.functions.segments import coalesce_short_transcript_segments
from backend.ops.podcast.operators import (
    populate_podcast_metadata
)
from backend.api.utils import debug_logger

from backend.src.podcast.functions.helpers import sorting_key
from backend.ops.storage import get_episode_metadata_path, get_podcast_metadata_path, get_transcript_path
#########################################################################################

PODCAST_ROUTER = APIRouter(
    prefix="/api/podcast",
    tags=["podcast"],
    responses={404: {"description": "Not found"}},
)

#########################################################################################

@PODCAST_ROUTER.get("/the_podcast")
async def podcasts_endpoint(request: Request):
    import dataclasses
    return [THE_PODCAST]

@PODCAST_ROUTER.post("/{podcast_id}")
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

@PODCAST_ROUTER.get("/{podcast_id}")
async def podcast_endpoint(podcast_id: str):
    debug_logger()
    print("-------------------------------------------------------------------------------------------TESTING UPDATE")
    previously_stored = True

    pod_metadata_path = get_podcast_metadata_path(podcast_id)
    debug_logger(message=f"pod_metadata_path: {pod_metadata_path}")
    # BUG: don't just check if it exists, check if it is of correct structure, not empty etc. and then if it isn't repopulate, else load it
    #if not pod_metadata_path.exists():
    #    previously_stored = False
    #    print("Tries to repopulate")
    #    await repopulate_metadata(podcast_id)
        # return dict(error="Podcast metadata not preloaded.")
    await repopulate_metadata(podcast_id)

    ep_metadata_path = get_episode_metadata_path(podcast_id)
    #if not ep_metadata_path.exists():
    #    previously_stored = False
    #    await repopulate_metadata(podcast_id)
        
    with open(pod_metadata_path, "r") as f:
        pod_metadata = json.load(f)

    episodes = {}
    with open(ep_metadata_path, 'r') as f: # NOTE: swap these types of calls out for a generic `write_to_storage(remote_path, dataload)`
        episodes = json.load(f)
    debug_logger(message=f"Loaded {len(episodes)} episodes.")
    episodes = {k: v for k, v in sorted(episodes.items(), key=sorting_key, reverse=True)} # NOTE: preferably the data structure should already be determined by the modal function producing this & we can typehint at locations like this for what's returned after json.load()
    
    # Refresh possibly stale data asynchronously.
    if previously_stored:
        populate_podcast_metadata.spawn(podcast_id)

    return dict(pod_metadata=pod_metadata, episodes=episodes)

@PODCAST_ROUTER.get("/{podcast_id}/episode/{episode_number}")
async def get_episode(podcast_id: str, episode_number: str):
    debug_logger()

    # Load all episodes
    ep_metadata_path = get_episode_metadata_path(podcast_id)
    with open(ep_metadata_path, 'r') as f:
        episodes = json.load(f)

    # Find the episode with the matching number
    try:
        episode = episodes[episode_number]
    except KeyError:
        debug_logger(message=f"Episode not found.")
        raise HTTPException(status_code=404, detail="Episode not found")

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