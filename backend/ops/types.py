from typing import NamedTuple

class InProgressJob(NamedTuple):
    job_id: str
    start_time: int