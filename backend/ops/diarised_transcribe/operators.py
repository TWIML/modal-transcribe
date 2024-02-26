import pathlib, json

from typing import Union

from backend.ops import storage
from backend.ops.stub import stub
from backend.ops.image import APP_IMAGE
from backend.ops.storage import APP_VOLUME, get_episode_metadata_path

from backend.src.podcast.types import EpisodeMetadata
from backend.src.podcast.functions.download import store_original_audio

from backend.src.diarised_transcribe.diariser import PyannoteDiariser
from backend.src.diarised_transcribe.types import DiarisationResult

from backend._utils import get_logger; logger = get_logger(__name__)

@stub.function(
    gpu='any',
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    timeout=900,
)
def diarise_episode(
    audio_filepath: pathlib.Path,
    hf_access_token: str
) -> DiarisationResult:
    """
    Just executes the `src` diarisation functionality given
    the audio path
    """
    # BUG/NOTE: I'm not sure how the imports will play
    # out or if they will propagate downwards to the
    # PyannoteDiariser

    diariser = PyannoteDiariser(hf_access_token=hf_access_token)
    filepath = audio_filepath.as_posix()
    diarisation_result = diariser.diarise(filepath=filepath)
    return diarisation_result

@stub.function(
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    timeout=900,
)
def download_podcast_audio_to_modal(podcast_id: str, episode_number: str):
    """
    Given an episode number and podcast id download the
    audio of it to modal storage location

    NOTE: should generalise this and store in a _utils 
    folder/file or base class etc.
    """
    import dacite
    # Downloading the audio
    storage.RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    metadata_path = get_episode_metadata_path(podcast_id)
    with open(metadata_path, "r") as f:
        data = json.load(f)
        data = data[episode_number]
        logger.info(data)
        episode = dacite.from_dict(
            data_class=EpisodeMetadata, data=data
        )
    audio_store_path = storage.RAW_AUDIO_DIR / episode.guid_hash
    store_original_audio(
        url=episode.audio_download_url,
        destination=audio_store_path,
    )
    return audio_store_path


# NOTE: the settings for function come up so much
# should just use a modal class instead and wrap
# like functionality up into it
@stub.function(
    gpu='any',
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    timeout=900,
)
def trigger_diarisation(
    podcast_id: str, 
    episode_number: str, 
    hf_access_token: str
) -> Union[DiarisationResult, None]:
    try:
        # download the audio
        audio_store_path = (
            download_podcast_audio_to_modal.remote(
                podcast_id=podcast_id,
                episode_number=episode_number
            )
        )

        # trigger the diarisation
        diarisation_result: Union[
            DiarisationResult,
            None
         ] = (
            diarise_episode.remote( # NOTE: spawn happens in the background, may be best to use that instead
                audio_filepath=audio_store_path,
                hf_access_token=hf_access_token
            ) # NOTE: job takes too long > 5 mins, even on cuda/gpu
        ) # NOTE: may want to split the audio file into segments in order to diarise - perhaps splitting on silences?
        # NOTE: would not be good to split on silence as speaker references will start switching

    except Exception as e:
        diarisation_result = None
        logger.warning("""
            Failed to diarise the audio
        """)
        
    return diarisation_result