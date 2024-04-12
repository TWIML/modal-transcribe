'''
Settings for different modal container types - specifying the requirements of running different functions
'''
from typing import TypedDict
from modal import Image
import modal

from backend.ops.image import APP_IMAGE
from backend.ops.storage import CACHE_DIR, APP_VOLUME

class ContainerSettingsType(TypedDict):
    gpu: str # 'any',
    image: Image # APP_IMAGE,
    network_file_systems: dict # {CACHE_DIR: APP_VOLUME},
    timeout: int # 900

SECRETS_NAME = "twiml-rag"

DOWNLOADING_PROCESSOR_CONTAINER_SETTINGS = ContainerSettingsType(
    gpu='any',
    image=APP_IMAGE,
    network_file_systems={CACHE_DIR:APP_VOLUME},
    timeout=900,
    secrets=[modal.Secret.from_name(SECRETS_NAME)]
)