import pathlib
from modal import NetworkFileSystem

from backend import config

APP_VOLUME = NetworkFileSystem.persisted("dataset-cache-vol")

def get_podcast_metadata_path(podcast_id: str) -> pathlib.Path:
    return config.PODCAST_METADATA_DIR / podcast_id / "metadata.json"

def get_episode_metadata_path(podcast_id: str) -> pathlib.Path:
    return config.PODCAST_METADATA_DIR / podcast_id / "episodes.json"

def get_transcript_path(guid_hash: str) -> pathlib.Path:
    return config.TRANSCRIPTIONS_DIR / f"{guid_hash}.json"