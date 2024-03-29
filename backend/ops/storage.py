import pathlib
from modal import NetworkFileSystem

from backend import backend_root_module_directory

APP_VOLUME = NetworkFileSystem.from_name("dataset-cache-vol")

####################
# Modal file paths
####################
CACHE_DIR = "/cache"
# Where downloaded podcasts are stored, by guid hash.
# Mostly .mp3 files 50-100MiB.
RAW_AUDIO_DIR = pathlib.Path(CACHE_DIR, "raw_audio")
# Stores metadata of individual podcast episodes as JSON.
PODCAST_METADATA_DIR = pathlib.Path(CACHE_DIR, "podcast_metadata")
# Completed episode transcriptions. Stored as flat files with
# files structured as '{guid_hash}-{model_slug}.json'.
TRANSCRIPTIONS_DIR = pathlib.Path(CACHE_DIR, "transcriptions")
# Diarisation store - intention is to store diarisations here and then use them to direct the transcriptions
DIARISATIONS_DIR = pathlib.Path(CACHE_DIR, "diarisations")
# Location of model checkpoint.
MODEL_DIR = pathlib.Path(CACHE_DIR, "model")
####################

####################
# Local file paths
####################
# Location of web frontend assets.
ASSETS_PATH = pathlib.Path(backend_root_module_directory).parent / "frontend" / "dist" #NOTE
####################


####################
# Helper path funcs
# for modal dirs
####################
def get_podcast_metadata_path(podcast_id: str) -> pathlib.Path:
    return PODCAST_METADATA_DIR / podcast_id / "metadata.json"

def get_episode_metadata_path(podcast_id: str) -> pathlib.Path:
    return PODCAST_METADATA_DIR / podcast_id / "episodes.json"

def get_transcript_path(guid_hash: str) -> pathlib.Path:
    return TRANSCRIPTIONS_DIR / f"{guid_hash}.json"

def get_diarisation_path(guid_hash: str) -> pathlib.Path:
    return DIARISATIONS_DIR / f"{guid_hash}.json"

def get_audio_path(guid_hash: str) -> pathlib.Path:
    return RAW_AUDIO_DIR / f"{guid_hash}"