from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Dict, Literal, Union

class DiarisedSegmentBounds(BaseModel):
    start: float
    end: float
    speaker: str # NOTE: Speaker_0 etc. (should make regex)

class DiarisationResult(BaseModel):
    speakers: List[str]
    segments: List[DiarisedSegmentBounds]

''' # eg. outputs from whisper
{
    'text': ' developing in since like', 
    'segments': 
        [
            {
                'id': 0, 
                'seek': 0, 
                'start': 0.0, 
                'end': 2.0, 
                'text': ' developing in since like', 
                'tokens': [50363, 5922, 287, 1201, 588, 50463], 
                'temperature': 0.0, 
                'avg_logprob': -0.6109485626220703, 'compression_ratio': 0.75, 
                'no_speech_prob': 0.4606165587902069
            }
        ], 
    'language': 'en'
}

{
    'text': " riff on how the year felt as an RL researcher. Yeah, that's a very...", 
    'segments': 
        [
            {
                'id': 0, 
                'seek': 0, 
                'start': 0.0, 
                'end': 3.6, 
                'text': ' riff on how the year felt as an RL researcher.', 'tokens': [50363, 36738, 319, 703, 262, 614, 2936, 355, 281, 45715, 13453, 13, 50543], 
                'temperature': 0.0, 
                'avg_logprob': -0.5380323658818784, 
                'compression_ratio': 0.9583333333333334, 'no_speech_prob': 0.08405435085296631
            }, 
            {
                'id': 1, 
                'seek': 0, 
                'start': 3.6, 
                'end': 4.16, 
                'text': " Yeah, that's a very...", 
                'tokens': [50543, 9425, 11, 326, 338, 257, 845, 986, 50571], 'temperature': 0.0, 
                'avg_logprob': -0.5380323658818784, 
                'compression_ratio': 0.9583333333333334, 
                'no_speech_prob': 0.08405435085296631
            }
        ], 
    'language': 'en'}
'''

class TranscriptionNestedSegment(BaseModel):
    id: int
    seek: int
    start: float 
    end: float
    text: str 
    tokens: List[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float 
    no_speech_prob: float

class TranscriptionResult(BaseModel):
    text: str
    segments: List[TranscriptionNestedSegment]
    language: str
    speaker: str

###############################################
# Below, building data-structs for our ui, above are
# forms returned from the models (pyannote, whisper)
###############################################
class FinalSegmentObject(BaseModel):
    start: float
    end: float
    text: str
    speaker: str

class FinalTranscriptionObject(BaseModel):
    text: str
    segments: List[FinalSegmentObject]

@dataclass
class TranscriptionDataClassReformer:
    items: List[TranscriptionResult]

    def reform(self) -> FinalTranscriptionObject:
        total_text = "" # not used on frontend
        __segments = [] # main data-struct
        for tr in self.items:
            total_text += tr.text
    
            # TODO: implement speaker coalescing
            # if speaker on this iteration same
            # as last one then don't append but
            # accumulate their data, else append
            first_start = tr.segments[0].start
            last_end = tr.segments[-1].end
            __segments.append(
                FinalSegmentObject(
                    start=first_start,
                    end=last_end,
                    text=tr.text,
                    speaker=tr.speaker
                )
            )
        return FinalTranscriptionObject(
            text=total_text,
            segments=__segments
        )
