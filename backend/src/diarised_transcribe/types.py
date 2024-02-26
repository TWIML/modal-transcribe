from pydantic import BaseModel
from typing import List, Dict, Literal, Union

segmentKeys = Literal[
    "start",
    "end",
    "speaker"
]

class DiarisedSegmentBounds(BaseModel):
    start: float
    end: float
    speaker: str # NOTE: Speaker_0 etc. (should make regex)

class DiarisationResult(BaseModel):
    speakers: List[str]
    segments: List[DiarisedSegmentBounds]