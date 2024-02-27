from backend.ops.storage import APP_VOLUME, get_transcript_path, get_episode_metadata_path
from backend.ops.image import APP_IMAGE
from backend.ops.stub import stub
from backend.ops import storage

from backend.src.podcast.functions.episodes import fetch_episodes as _fetch_episodes
from backend.src.podcast.types import EpisodeMetadata
from backend.src.podcast.constants import THE_PODCAST

import dataclasses, json

from backend import _utils; logger = _utils.get_logger(__name__)

@stub.function(network_file_systems={storage.CACHE_DIR: APP_VOLUME})
def populate_podcast_metadata(podcast_id = "twiml-ai-podcast"):
    logger.info(f"Updating episode metadata in the background.")

    metadata_dir = storage.PODCAST_METADATA_DIR / podcast_id
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    pod_metadata = THE_PODCAST

    pod_metadata_path = metadata_dir / "metadata.json"
    with open(pod_metadata_path, "w") as f:
        json.dump(dataclasses.asdict(pod_metadata), f)

    episodes: dict[str, EpisodeMetadata] = fetch_episodes.remote(
        url=pod_metadata.feed_url
    )

    for episode_number in episodes.keys():
        episodes[episode_number].transcribed = get_transcript_path(episodes[episode_number].guid_hash).exists()
            
    ep_metadata_path = get_episode_metadata_path(podcast_id)

    with open(ep_metadata_path, 'w') as f:
        json.dump({k: v.model_dump() for k, v in episodes.items()}, f)
    
    logger.info(f"Updated metadata for {len(episodes)} episodes of podcast {pod_metadata.id}.")

@stub.function(
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
)
def fetch_episodes(url: str) -> dict[str, EpisodeMetadata]:
    return _fetch_episodes(url=url)