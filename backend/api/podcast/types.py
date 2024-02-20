import dataclasses
from typing import Optional

@dataclasses.dataclass
class EpisodeMetadata:
    # Unique ID of podcast this episode is associated with.
    # podcast_id: Union[str, int]
    # Title of podcast this episode is associated with.
    # podcast_title: Optional[str]
    # Episode title
    title: str
    # Episide number (optional)
    episode_number: Optional[str]
    # The publish date of the episode as specified by the publisher
    publish_date: str
    # Plaintext description of episode. nb: has whitespace issues so not suitable in UI.
    description: str
    # HTML markup description. Suitable for display in UI.
    html_description: str
    # The unique identifier of this episode within the context of the podcast
    guid: str
    # Hash the guid into something appropriate for filenames.
    guid_hash: str
    # Link to episode on website.
    episode_url: Optional[str]
    # Link to audio file for episode. Typically an .mp3 file.
    audio_download_url: str
    # Whether the episode has been transcribed
    transcribed: bool = False