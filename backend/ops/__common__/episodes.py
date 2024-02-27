import json
from backend.ops.storage import get_episode_metadata_path

from backend.src.podcast.types import EpisodeMetadata

from backend._utils import get_logger; logger = get_logger(__name__)

def get_episode_metadata(podcast_id:str, episode_number: str) -> EpisodeMetadata:
    metadata_path = get_episode_metadata_path(podcast_id)
    with open(metadata_path, "r") as f:
        data = json.load(f)
        data = data[episode_number]
        logger.info(data)
        episode = EpisodeMetadata(**data)
    return episode