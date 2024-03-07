import json

from modal import method, enter, build
from typing import Union, List, Optional, Tuple
import pathlib

from backend.ops.stub import stub
from backend.ops.settings import DOWNLOADING_PROCESSOR_CONTAINER_SETTINGS
from backend.ops.diarised_transcribe.constants import DEFAULT_MODEL
from backend.ops.storage import MODEL_DIR, DIARISATIONS_DIR, TRANSCRIPTIONS_DIR, RAW_AUDIO_DIR, get_audio_path, get_diarisation_path, get_transcript_path

from backend.src.podcast.types import EpisodeMetadata
from backend.ops.__common__.episodes import get_episode_metadata # Should be in src

from backend.src.diarised_transcribe.diariser import PyannoteDiariser
from backend.src.diarised_transcribe.types import DiarisedSegmentBounds, DiarisationResult, TranscriptionResult, TranscriptionDataClassReformer, FinalTranscriptionObject
from backend.ops.__common__.downloads import download_podcast_audio as _download_podcast_audio

from backend.src.diarised_transcribe.transcriber import WhisperTranscriber

from backend._utils import get_logger; logger = get_logger(__name__)

# BUG: hardcoding model name and dirs, want to either pass these in from relevant api-request, or pull in from a config.yaml for model stuff that is on the top level of repo

@stub.cls(
**DOWNLOADING_PROCESSOR_CONTAINER_SETTINGS
)
class DiariseAndTranscribeModalOperator:
    
    # pre-set/hardcoded/default class atrrs
    model_name:str = DEFAULT_MODEL.name
    model_dir:pathlib.Path = MODEL_DIR
    
    @build()
    def container_build(self):
        print('--------------------------------------------BUILDING---------------------------------------------')
        self.transcription_model = (
            WhisperTranscriber \
                .download_model_to_path(
                    model_name=self.model_name,
                    model_dir=self.model_dir,
                    in_memory=False,
                )
        )

    @enter()
    def container_setup(self):
        print('------------------------------------------------SETTING UP------------------------------------------------')
        RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        DIARISATIONS_DIR.mkdir(parents=True, exist_ok=True)
        TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

    @method()
    def download_podcast_audio(
        self,
        podcast_id: str,
        episode_number: str,
        audio_store_path: pathlib.Path,
        overwrite_download: bool
    ) -> pathlib.Path:
        """
        Stores the audio at given path and returns path.
        """
        if (
            (not audio_store_path.exists()) 
            or overwrite_download
        ): # download whenever path not there, or if path there but overwrite specified
            audio_stored_path = _download_podcast_audio(
                podcast_id=podcast_id, 
                episode_number=episode_number,
                overwrite_download=overwrite_download
            )
        else:
            audio_stored_path = audio_store_path
        return audio_stored_path

    @method()
    def diarise_episode(
        self,
        audio_file_path: pathlib.Path,
        hf_access_token: str
    ) -> DiarisationResult:
        """
        Executes `src` diarisation functionality given
        the audio path & returns a list of the diarised
        segments.
        """
        print('------------------IN DIARISE EPISODE-------------------------------')
        diariser = PyannoteDiariser(hf_access_token=hf_access_token)
        diarisation_result = diariser.diarise(
            audio_file_path=audio_file_path
        )
        return diarisation_result

    @method()
    def trigger_diarisation(
        self,
        podcast_id: str, 
        episode_number: str, 
        hf_access_token: str,
        audio_stored_path: pathlib.Path,
        diarisation_store_path: pathlib.Path,
        overwrite_diarisation: bool
    ) -> Optional[DiarisationResult]:
        '''
        Triggers the end-to-end diarisation process by
        calling it's sibling methods: 
            `download_podcast_audio` &
            `diarise_episode`
        
        If diarisation is already done it loads it from
        json to the data structure.
        '''
        try:
            if (
                (not diarisation_store_path.exists())
                or overwrite_diarisation
            ): # if doesn't exist already run, if does but overwrite is specified then run as well
                # trigger the diarisation
                diarisation_result: DiarisationResult = (
                    self.diarise_episode.remote( # NOTE: spawn happens in the background, may be best to use that instead
                        audio_file_path=audio_stored_path,
                        hf_access_token=hf_access_token
                    ) # NOTE: job takes too long > 5 mins, even on cuda/gpu
                )
                with open(diarisation_store_path, "w") as f:
                    f.write(
                        diarisation_result.model_dump_json()
                    )
                logger.info(f"**Wrote diarisation to {diarisation_store_path}** \n\t ... diarisation output -> {diarisation_result.model_dump_json()}")
            else:
                with open(diarisation_store_path, "r") as f:
                    diarisation_dict = json.load(f)
                    diarisation_result = DiarisationResult(
                        **diarisation_dict
                    )
                    logger.info(f"**Diarisation already existed, loaded diarisation from {diarisation_store_path}**")

        except Exception as e:
            diarisation_result = None # type: ignore
            logger.warn(f"""
                Failed to diarise the audio see the exception:
                        {e}
            """)
            
        return diarisation_result
    
    @method()
    def transcribe_segment(
        self,
        diarised_segment_bounds: DiarisedSegmentBounds,
        audio_file_path: pathlib.Path
    ) -> TranscriptionResult:
        '''
        Executes `src` transcription functionality given the
        audio path & the diarised segment bounds (start, end
        times & speaker for that segment)
        '''
        print(f"""
            Checking model name & dir:
                {self.model_name, self.model_dir}
        """)
        transcription_result = (
            WhisperTranscriber.transcribe_segment(
                diarised_segment_bounds=diarised_segment_bounds,
                audio_file_path=audio_file_path,
                model_name=self.model_name,
                model_dir=self.model_dir
            )
        )
        return transcription_result

    
    @method()
    def trigger_transcription(
        self,
        diarised_segments: List[DiarisedSegmentBounds],
        audio_file_path: pathlib.Path,
        transcription_store_path: pathlib.Path,
        overwrite_transcription: bool
    ) -> Optional[FinalTranscriptionObject]:
        '''
        Distributes the transcription job across all diarised
        segments and returns the collected results

        NOTE: returns a list of transcribed diarised segments
        i.e. for an audio file - it is first diarised (speaker's 
        are annotated) and then segmented by the speaker segments
        (start and end time of a speaker's segment) - these are
        then transcribed and collected into an iterable and returned.
        '''
        try:
            if (
                (not transcription_store_path.exists())
                or overwrite_transcription
            ): # execute when path not there or if there but overwrite specified
                transcribed_segments = list(
                    self.transcribe_segment.map(
                        diarised_segments, 
                        kwargs=dict(
                            audio_file_path=audio_file_path
                        ),
                        return_exceptions=True # NOTE:doesn't fail on errors
                ))
                transcription_result: FinalTranscriptionObject = TranscriptionDataClassReformer(
                    items=transcribed_segments
                ).reform()
                for _ in transcribed_segments:
                    print(_)
                with open(transcription_store_path, "w") as f:
                    f.write(
                        transcription_result.model_dump_json()
                    )
                logger.info(f"**Wrote transcription to {transcription_store_path}** \n\t ... transcription output -> {transcription_result.model_dump_json()}")
            else: # load from disk
                with open(transcription_store_path, "r") as f:
                    transcription_dict = json.load(f)
                    transcription_result = FinalTranscriptionObject(
                        **transcription_dict
                    )
                    logger.info(f"**Transcription already existed, loaded transcription from {transcription_store_path}**")
        except Exception as e:
            transcription_result = None # type: ignore
            logger.warn(f"""
                Transcription failed with error: 
                        {e}
            """)
            
        return transcription_result
    
    @method()
    def trigger_process(
        self, 
        podcast_id: str, 
        episode_number: str, 
        hf_access_token: str,
        overwrite_download: bool,
        overwrite_diarisation: bool,
        overwrite_transcription: bool
    ) -> Optional[FinalTranscriptionObject]:
        '''
        Triggers the end to end diarisation &
        transcription process
        '''
        ############################################
        # file setup etc.
        ############################################
        episode: EpisodeMetadata = get_episode_metadata(
            podcast_id=podcast_id,
            episode_number=episode_number
        )
        audio_store_path = get_audio_path(episode.guid_hash)
        diarisation_store_path = get_diarisation_path(episode.guid_hash)
        transcription_store_path = get_transcript_path(episode.guid_hash)
        ############################################
        self.download_podcast_audio.remote(
            podcast_id=podcast_id,
            episode_number=episode_number,
            audio_store_path=audio_store_path,
            overwrite_download=overwrite_download
        )
        ############################################
        diarisation_result = self.trigger_diarisation.remote(
            podcast_id=podcast_id,
            episode_number=episode_number,
            hf_access_token=hf_access_token,
            audio_stored_path=audio_store_path,
            diarisation_store_path=diarisation_store_path,
            overwrite_diarisation=overwrite_diarisation
        )
        ############################################
        if diarisation_result:
            diarised_segments=diarisation_result.segments
            final_transcription: FinalTranscriptionObject = self.trigger_transcription.remote(
                diarised_segments=diarised_segments,
                audio_file_path=audio_store_path,
                transcription_store_path=transcription_store_path,
                overwrite_transcription=overwrite_transcription
            )
        else:
            final_transcription = None # type: ignore
            # Must have been failure during diarise
            # should we raise an exception there
            # instead
            logger.warning(f"""
                Failed to diarise the audio
            """)
        
        return final_transcription