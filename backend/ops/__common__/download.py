import json
from backend.ops.storage import RAW_AUDIO_DIR, get_episode_metadata_path

from backend.src.podcast.types import EpisodeMetadata
from backend.src.podcast.functions.download import store_original_audio

from backend._utils import get_logger; logger = get_logger(__name__)

def download_podcast_audio(podcast_id: str, episode_number: str):
    """
    Given an episode number and podcast id download the
    audio of it to modal storage location
    """
    # Downloading the audio
    RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    metadata_path = get_episode_metadata_path(podcast_id)
    with open(metadata_path, "r") as f:
        data = json.load(f)
        data = data[episode_number]
        logger.info(data)
        episode = EpisodeMetadata(**data)
    audio_store_path = RAW_AUDIO_DIR / episode.guid_hash
    store_original_audio(
        url=episode.audio_download_url,
        destination=audio_store_path,
    )
    return audio_store_path