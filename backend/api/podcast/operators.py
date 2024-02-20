from backend.app.storage import APP_VOLUME, get_transcript_path, get_episode_metadata_path
from backend.app.image import APP_IMAGE
from backend.app.functions import stub
from backend import config

from backend.api.podcast.functions.episodes import fetch_episodes as _fetch_episodes
from backend.src.podcast import the_podcast

import dataclasses, json

logger = config.get_logger(__name__)

@stub.function(network_file_systems={config.CACHE_DIR: APP_VOLUME})
def populate_podcast_metadata(podcast_id = "twiml-ai-podcast"):
    logger.info(f"Updating episode metadata in the background.")

    metadata_dir = config.PODCAST_METADATA_DIR / podcast_id
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    pod_metadata = the_podcast

    pod_metadata_path = metadata_dir / "metadata.json"
    with open(pod_metadata_path, "w") as f:
        json.dump(dataclasses.asdict(pod_metadata), f)

    episodes = fetch_episodes.remote(
        url=pod_metadata.feed_url
    )

    for episode_number in episodes.keys():
        episodes[episode_number].transcribed = get_transcript_path(episodes[episode_number].guid_hash).exists()
            
    ep_metadata_path = get_episode_metadata_path(podcast_id)

    with open(ep_metadata_path, 'w') as f:
        json.dump({k: dataclasses.asdict(v) for k, v in episodes.items()}, f)
    
    logger.info(f"Updated metadata for {len(episodes)} episodes of podcast {pod_metadata.id}.")

@stub.function(
    image=APP_IMAGE,
    network_file_systems={config.CACHE_DIR: APP_VOLUME},
)
def fetch_episodes(url: str):
    return _fetch_episodes(url=url)