import os
from pyannote.audio import Pipeline, Audio
import torch, pathlib

from typing import List, Dict
from backend.src.diarised_transcribe.types import DiarisedSegmentBounds, DiarisationResult

from backend._utils import get_logger

logger = get_logger(__name__)

class PyannoteDiariser:

    def diarise(
        self, 
        audio_file_path: pathlib.Path
    ) -> DiarisationResult:
        # Retrieve model pipeline from HF
        print('------------------------ABOUT TO HIT THE PIPELINE------------------------------')
        pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization',
            use_auth_token=os.environ['HUGGING_FACE_API_KEY']
        )

        # Run on Cuda device if available
        use_gpu = torch.cuda.is_available()
        device = 'cuda' if use_gpu else 'cpu'
        logger.info(f"""
            Pyannote Diariser is running on
                 device type: {device}
        """)
        pipeline.to(torch.device(device))

        # Changing filepath to string
        audio_file_path_str = audio_file_path.as_posix()
        # Load the audio file and downmix and downsample it
        io = Audio(mono='downmix', sample_rate=16000)
        waveform, sample_rate = io(audio_file_path_str)

        # Put it through the pipeline to diarise
        diarisation = pipeline({
            "waveform": waveform, 
            "sample_rate": sample_rate
        })

        # Restructure the output
        diarisation_dict: Dict[str, list] = {
            'speakers': [],
            'segments': []
        }
        speakers_set = set()
        for segment, label, speaker in diarisation.itertracks(yield_label=True):
            speakers_set.add(speaker)
            dseg = DiarisedSegmentBounds(
                start=segment.start,
                end=segment.end,
                speaker=speaker
            )
            diarisation_dict['segments'].append(dseg)
        diarisation_dict['speakers'] = list(speakers_set)

        return DiarisationResult(**diarisation_dict)