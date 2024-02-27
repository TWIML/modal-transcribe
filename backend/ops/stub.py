import modal
from typing import Dict

from backend.ops.image import APP_IMAGE

stub = modal.Stub(
    "whisper-pod-transcriber",
    image=APP_IMAGE
)

stub.in_progress = modal.Dict.new()