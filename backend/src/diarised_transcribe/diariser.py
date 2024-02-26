from pyannote.audio import Pipeline, Audio
import torch

from typing import Dict
from backend.src.diarised_transcribe.types import DiarisationResult

from backend._utils import get_logger

logger = get_logger(__name__)

class PyannoteDiariser:

    def __init__(self, hf_access_token: str):
        self.hf_access_token = hf_access_token

    def diarise(self, filepath: str) -> DiarisationResult:
        # Retrieve model pipeline from HF
        pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization',
            use_auth_token=self.hf_access_token
        )

        # Run on Cuda device if available
        use_gpu = torch.cuda.is_available()
        device = 'cuda' if use_gpu else 'cpu'
        logger.info(f"""
            Pyannote Diariser is running on
                 device type: {device}
        """)
        pipeline.to(torch.device(device))

        # Load the audio file and downmix and downsample it
        io = Audio(mono='downmix', sample_rate=16000)
        waveform, sample_rate = io(filepath)

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
            diarisation_dict['segments'].append({
                'start': segment.start,
                'end': segment.end,
                'speaker': speaker
            })
        diarisation_dict['speakers'] = list(speakers_set)
        return DiarisationResult(**diarisation_dict)