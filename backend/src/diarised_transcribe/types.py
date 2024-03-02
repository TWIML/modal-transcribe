from pydantic import BaseModel
from typing import List, Dict, Literal, Union

class DiarisedSegmentBounds(BaseModel):
    start: float
    end: float
    speaker: str # NOTE: Speaker_0 etc. (should make regex)

class DiarisationResult(BaseModel):
    speakers: List[str]
    segments: List[DiarisedSegmentBounds]

'''
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

class CompletedTranscriptObject(BaseModel):
    items: List[TranscriptionResult]