import urllib.request
import re, hashlib
import xml.etree.ElementTree as ET

from backend.src.podcast.types import EpisodeMetadata

from backend.ops import storage
from backend import _utils; logger = _utils.get_logger(__name__)

def fetch_episodes(url) -> dict[str, EpisodeMetadata]:
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