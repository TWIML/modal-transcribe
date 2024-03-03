import pathlib
from backend.ops.storage import RAW_AUDIO_DIR

from backend.ops.__common__.episodes import get_episode_metadata
from backend.src.podcast.functions.download import store_original_audio

from backend._utils import get_logger; logger = get_logger(__name__)

def download_podcast_audio(
    podcast_id: str, 
    episode_number: str,
    overwrite_download: bool
) -> pathlib.Path:
    """
    Given an episode number and podcast id download the
    audio of it to modal storage location
    """
    # Downloading the audio
    RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    episode = get_episode_metadata(podcast_id=podcast_id, episode_number=episode_number)
    audio_store_path = RAW_AUDIO_DIR / episode.guid_hash
    store_original_audio(
        url=episode.audio_download_url,
        destination=audio_store_path,
        overwrite=overwrite_download
    )
    return audio_store_path