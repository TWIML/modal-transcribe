import dataclasses
import xml.etree.ElementTree as ET
import os
import pathlib
import re
import urllib.request
from typing import NamedTuple, Optional, TypedDict, Union
import hashlib

from . import config

logger = config.get_logger(__name__)
Segment = TypedDict("Segment", {"text": str, "start": float, "end": float})


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


@dataclasses.dataclass
class PodcastMetadata:
    # Unique ID for a podcast
    id: str
    # Title of podcast, eg. 'The Joe Rogan Experience'.
    title: str
    # Plaintext description of episode. nb: has whitespace issues so not suitable in UI.
    description: str
    html_description: str
    # Link to podcast homepage.
    web_url: str
    # Feed url
    feed_url: str
    # Used to detect non-English podcasts.
    language: Optional[str] = None


the_podcast = PodcastMetadata(
    id="twiml-ai-podcast",
    title="The TWIML AI Podcast",
    description="description",
    html_description="htmlDescription",
    web_url="https://twimlai.com",
    feed_url="https://twimlai.com/feed/"
)


class DownloadResult(NamedTuple):
    data: bytes
    # Helpful to store and transmit when uploading to cloud bucket.
    content_type: str

def download_podcast_file(url: str) -> DownloadResult:
    req = urllib.request.Request(
        url,
        data=None,
        # Set a user agent to avoid 403 response from some podcast audio servers.
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        },
    )
    with urllib.request.urlopen(req) as response:
        return DownloadResult(
            data=response.read(),
            content_type=response.headers["content-type"],
        )

def fetch_episodes(url) -> dict:
    """
    Get RSS feed and parse list of episodes
    :param rss_url: URL of the RSS feed
    :return: List of dictionaries where each dictionary is a podcast episode
    """
    logger.info(f"Fetching Podcast RSS Feed from {url}.")

    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
    except urllib.error.URLError as e:
        logger.error(f"ERROR: Failed to fetch RSS feed from {url}. Error: {e}")
        return None
    
    # Define the namespace
    namespaces = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}

    logger.info(f"Extracting episode metadata from feed.")

    # Parse the XML content
    tree = ET.fromstring(content)

    episodes = {}

    for item in tree.findall('./channel/item'):
        title = item.find('title').text
        description = item.find('description').text
        # Try to extract the episode number
        try:
            episode_number = item.find("itunes:episode", namespaces).text
        except (TypeError, ValueError, AttributeError):
            # If itunes:episode field is not available, try to extract the episode number from the title
            try:
                title_parts = title.split(' ')
                episode_number = int(title_parts[-1].replace('#', ''))
                # Check if the title starts with an open parenthesis, if so it's unluck episode 18
                if title_parts[0][0] == '(':
                    part_number = int(title_parts[0].split('/')[0].replace('(', ''))
                    episode_number = f"{episode_number}.{part_number}"
            except ValueError:
                # One last try, let's look for a show notes URL in the description and try to grab the episode number from there
                # This is for episode 88 which is somehow published w/out an episode number
                match = re.search(r'twimlai\.com/(talk|go)/(\d+)', description)
                if match:
                    episode_number = match.group(2)
                else:
                    logger.warning(f"WARNING: Failed to extract episode number from title: {title}")    
                    continue  # Skip this episode if we can't extract an episode number
        title = title.rsplit('-', 1)[0].strip()
        publish_date = item.find('pubDate').text
        html_description = item.find('content:encoded').text if item.find('content:encoded') is not None else description
        guid = item.find('guid').text
        guid_hash = hashlib.md5(guid.encode('utf-8')).hexdigest()
        episode_url = item.find('link').text
        audio_download_url = item.find('enclosure').get('url')

        episodes[episode_number] = EpisodeMetadata(
            title=title,
            episode_number=episode_number,
            publish_date=publish_date,
            description=description,
            html_description=html_description,
            guid=guid,
            guid_hash=guid_hash,
            episode_url=episode_url,
            audio_download_url=audio_download_url
        )

    logger.info(f"Extracted {len(episodes)} episodes.")
    return episodes


def sizeof_fmt(num, suffix="B") -> str:
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def store_original_audio(
    url: str, destination: pathlib.Path, overwrite: bool = False
) -> None:
    if destination.exists():
        if overwrite:
            logger.info(
                f"Audio file exists at {destination} but overwrite option is specified."
            )
        else:
            logger.info(
                f"Audio file exists at {destination}, skipping download."
            )
            return

    podcast_download_result = download_podcast_file(url=url)
    humanized_bytes_str = sizeof_fmt(num=len(podcast_download_result.data))
    logger.info(f"Downloaded {humanized_bytes_str} episode from URL.")
    with open(destination, "wb") as f:
        f.write(podcast_download_result.data)
    logger.info(f"Stored audio episode at {destination}.")


def coalesce_short_transcript_segments(
    segments: list[Segment],
) -> list[Segment]:
    """
    Some extracted transcript segments from openai/whisper are really short, like even just one word.
    This function accepts a minimum segment length and combines short segments until the minimum is reached.
    """
    minimum_transcript_len = 200  # About 2 sentences.
    previous = None
    long_enough_segments = []
    for current in segments:
        if previous is None:
            previous = current
        elif len(previous["text"]) < minimum_transcript_len:
            previous = _merge_segments(left=previous, right=current)
        else:
            long_enough_segments.append(previous)
            previous = current
    if previous:
        long_enough_segments.append(previous)
    return long_enough_segments


def _merge_segments(left: Segment, right: Segment) -> Segment:
    return {
        "text": left["text"] + " " + right["text"],
        "start": left["start"],
        "end": right["end"],
    }
