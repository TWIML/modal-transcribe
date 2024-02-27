import whisper

from modal import method, enter, build
from typing import Union
import pathlib

from backend.ops.stub import stub
from backend.ops.settings import DOWNLOADING_PROCESSOR_CONTAINER_SETTINGS
from backend.ops.diarised_transcribe.constants import DEFAULT_MODEL
from backend.ops.storage import MODEL_DIR, DIARISATIONS_DIR, TRANSCRIPTIONS_DIR

from backend.src.diarised_transcribe.diariser import PyannoteDiariser
from backend.src.diarised_transcribe.types import DiarisationResult
from backend.ops.__common__.downloads import download_podcast_audio as _download_podcast_audio

from backend.src.diarised_transcribe.transcriber import WhisperTranscriber

from backend._utils import get_logger; logger = get_logger(__name__)

@stub.cls(
**DOWNLOADING_PROCESSOR_CONTAINER_SETTINGS
)
class DiariseAndTranscribeModalOperator:

    @build()
    def container_build(self):
        print('--------------------------------------------BUILDING---------------------------------------------')
        self.transcription_model = (
            WhisperTranscriber \
                .download_model_to_path(
                    model_name=DEFAULT_MODEL.name,
                    model_dir=MODEL_DIR,
                    in_memory=False,
                )
        )

    @enter()
    def container_setup(self):
        print('------------------------------------------------SETTING UP------------------------------------------------')
        DIARISATIONS_DIR.mkdir(parents=True, exist_ok=True)
        TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

    @method()
    def download_podcast_audio(
        self,
        podcast_id,
        episode_number  
    ):
        audio_stored_path = _download_podcast_audio(
            podcast_id=podcast_id, 
            episode_number=episode_number
        )
        return audio_stored_path

    @method()
    def diarise_episode(
        self,
        audio_filepath: pathlib.Path,
        hf_access_token: str
    ) -> DiarisationResult:
        """
        Just executes the `src` diarisation functionality given
        the audio path
        """

        diariser = PyannoteDiariser(hf_access_token=hf_access_token)
        filepath = audio_filepath.as_posix()
        diarisation_result = diariser.diarise(filepath=filepath)
        return diarisation_result

    @method()
    def trigger_diarisation(
        self,
        podcast_id: str, 
        episode_number: str, 
        hf_access_token: str
    ) -> Union[DiarisationResult, None]:
        try:
            # download the audio
            audio_stored_path = (
                self.download_podcast_audio.remote(
                    podcast_id=podcast_id,
                    episode_number=episode_number
                )
            )

            # trigger the diarisation
            diarisation_result: Union[
                DiarisationResult,
                None
            ] = (
                self.diarise_episode.remote( # NOTE: spawn happens in the background, may be best to use that instead
                    audio_filepath=audio_stored_path,
                    hf_access_token=hf_access_token
                ) # NOTE: job takes too long > 5 mins, even on cuda/gpu
            )

        except Exception as e:
            diarisation_result = None
            logger.warning("""
                Failed to diarise the audio
            """)
            
        return diarisation_result