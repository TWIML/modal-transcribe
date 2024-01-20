"""
whisper-pod-transcriber uses OpenAI's Whisper modal to do speech-to-text transcription
of podcasts.
"""
import dataclasses
import datetime
import json
import pathlib
import itertools
from typing import Iterator, Tuple

from modal import (
    Dict,
    Image,
    Mount,
    NetworkFileSystem,
    Period,
    Secret,
    Stub,
    asgi_app,
)

from . import config, podcast

logger = config.get_logger(__name__)
volume = NetworkFileSystem.persisted("dataset-cache-vol")

app_image = (
    Image.debian_slim()
    .apt_install("git")
    .pip_install(
        "git+https://github.com/openai/whisper.git",
        "dacite",
        "jiwer",
        "ffmpeg-python",
        "gql[all]~=3.0.0a5",
        "pandas",
        "loguru==0.6.0",
        "torchaudio==2.1.0",
    )
    .apt_install("ffmpeg")
    .pip_install("ffmpeg-python")
)
search_image = Image.debian_slim().pip_install(
    "scikit-learn~=1.3.0",
    "tqdm~=4.46.0",
    "numpy~=1.23.3",
    "dacite",
)

stub = Stub(
    "whisper-pod-transcriber",
    image=app_image,
    # secrets=[Secret.from_name("podchaser")],
)

stub.in_progress = Dict.new()


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

def get_podcast_metadata_path(podcast_id: str) -> pathlib.Path:
    return config.PODCAST_METADATA_DIR / podcast_id / "metadata.json"

def get_episode_metadata_path(podcast_id: str) -> pathlib.Path:
    return config.PODCAST_METADATA_DIR / podcast_id / "episodes.json"


def get_transcript_path(guid_hash: str) -> pathlib.Path:
    return config.TRANSCRIPTIONS_DIR / f"{guid_hash}.json"


@stub.function(network_file_systems={config.CACHE_DIR: volume})
def populate_podcast_metadata(podcast_id = "twiml-ai-podcast"):
    logger.info(f"Updating episode metadata in the background.")

    metadata_dir = config.PODCAST_METADATA_DIR / podcast_id
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    pod_metadata = podcast.the_podcast

    pod_metadata_path = metadata_dir / "metadata.json"
    with open(pod_metadata_path, "w") as f:
        json.dump(dataclasses.asdict(pod_metadata), f)

    episodes = fetch_episodes.remote(
        url=pod_metadata.feed_url
    )

    for episode_number in episodes.keys():
        episodes[episode_number].transcribed = get_transcript_path(episodes[episode_number].guid_hash).exists()
            
    ep_metadata_path = get_episode_metadata_path(podcast_id)

    with open(ep_metadata_path, 'w') as f:
        json.dump({k: dataclasses.asdict(v) for k, v in episodes.items()}, f)

    # Print a snippet of the episode metadata
    # with open(ep_metadata_path, 'r') as f:
    #     data = json.load(f)
    #     snippet = dict(itertools.islice(data.items(), 5))  # Get the first 5 items
    #     logger.info(json.dumps(snippet, indent=4))  # Print the snippet
    
    logger.info(f"Updated metadata for {len(episodes)} episodes of podcast {pod_metadata.id}.")


@stub.function(
    mounts=[Mount.from_local_dir(config.ASSETS_PATH, remote_path="/assets")],
    network_file_systems={config.CACHE_DIR: volume},
    keep_warm=2,
)
@asgi_app()
def fastapi_app():
    import fastapi.staticfiles

    from .api import web_app

    web_app.mount(
        "/", fastapi.staticfiles.StaticFiles(directory="/assets", html=True)
    )

    return web_app


@stub.function(
    image=search_image,
    schedule=Period(hours=4),
    network_file_systems={config.CACHE_DIR: volume},
    timeout=(400 * 60),
)
def refresh_index():
    import dataclasses
    from collections import defaultdict

    import dacite

    logger.info(f"Running scheduled index refresh at {utc_now()}")
    config.SEARCH_DIR.mkdir(parents=True, exist_ok=True)

    episodes = defaultdict(list)
    guid_hash_to_episodes = {}

    for pod_dir in config.PODCAST_METADATA_DIR.iterdir():
        if not pod_dir.is_dir():
            continue

        for filepath in pod_dir.iterdir():
            if filepath.name == "metadata.json":
                continue

            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
            except json.decoder.JSONDecodeError:
                logger.warning(
                    f"Removing corrupt JSON metadata file: {filepath}."
                )
                filepath.unlink()

            ep = dacite.from_dict(data_class=podcast.EpisodeMetadata, data=data)
            episodes[ep.podcast_title].append(ep)
            guid_hash_to_episodes[ep.guid_hash] = ep

    logger.info(f"Loaded {len(guid_hash_to_episodes)} podcast episodes.")

    transcripts = {}
    if config.TRANSCRIPTIONS_DIR.exists():
        for file in config.TRANSCRIPTIONS_DIR.iterdir():
            with open(file, "r") as f:
                data = json.load(f)
                guid_hash = file.stem.split("-")[0]
                transcripts[guid_hash] = data

    # Important: These have to be the same length and have same episode order.
    # i-th element of indexed_episodes is the episode indexed by the i-th element
    # of search_records
    indexed_episodes = []
    search_records = []
    for key, value in transcripts.items():
        idxd_episode = guid_hash_to_episodes.get(key)
        if idxd_episode:
            search_records.append(
                search.SearchRecord(
                    title=idxd_episode.title,
                    text=value["text"],
                )
            )
            # Prepare records for JSON serialization
            indexed_episodes.append(dataclasses.asdict(idxd_episode))

    logger.info(
        f"Matched {len(search_records)} transcripts to episode records."
    )

    filepath = config.SEARCH_DIR / "all.json"
    logger.info(f"writing {filepath}")
    with open(filepath, "w") as f:
        json.dump(indexed_episodes, f)

    logger.info(
        "calc feature vectors for all transcripts, keeping track of similar podcasts"
    )
    X, v = search.calculate_tfidf_features(search_records)
    sim_svm = search.calculate_similarity_with_svm(X)
    filepath = config.SEARCH_DIR / "sim_tfidf_svm.json"
    logger.info(f"writing {filepath}")
    with open(filepath, "w") as f:
        json.dump(sim_svm, f)

    logger.info("calculate the search index to support search")
    search_dict = search.build_search_index(search_records, v)
    filepath = config.SEARCH_DIR / "search.json"
    logger.info(f"writing {filepath}")
    with open(filepath, "w") as f:
        json.dump(search_dict, f)


def split_silences(
    path: str, min_segment_length: float = 30.0, min_silence_length: float = 1.0
) -> Iterator[Tuple[float, float]]:
    """Split audio file into contiguous chunks using the ffmpeg `silencedetect` filter.
    Yields tuples (start, end) of each chunk in seconds."""

    import re

    import ffmpeg

    silence_end_re = re.compile(
        r" silence_end: (?P<end>[0-9]+(\.?[0-9]*)) \| silence_duration: (?P<dur>[0-9]+(\.?[0-9]*))"
    )

    metadata = ffmpeg.probe(path)
    duration = float(metadata["format"]["duration"])

    reader = (
        ffmpeg.input(str(path))
        .filter("silencedetect", n="-10dB", d=min_silence_length)
        .output("pipe:", format="null")
        .run_async(pipe_stderr=True)
    )

    cur_start = 0.0
    num_segments = 0

    while True:
        line = reader.stderr.readline().decode("utf-8")
        if not line:
            break
        match = silence_end_re.search(line)
        if match:
            silence_end, silence_dur = match.group("end"), match.group("dur")
            split_at = float(silence_end) - (float(silence_dur) / 2)

            if (split_at - cur_start) < min_segment_length:
                continue

            yield cur_start, split_at
            cur_start = split_at
            num_segments += 1

    # silencedetect can place the silence end *after* the end of the full audio segment.
    # Such segments definitions are negative length and invalid.
    if duration > cur_start and (duration - cur_start) > min_segment_length:
        yield cur_start, duration
        num_segments += 1
    logger.info(f"Split {path} into {num_segments} segments")


@stub.function(
    image=app_image,
    network_file_systems={config.CACHE_DIR: volume},
    cpu=4,
    # gpu="any",
    timeout=600,
)
def transcribe_segment(
    start: float,
    end: float,
    audio_filepath: pathlib.Path,
    model: config.ModelSpec,
):
    import tempfile
    import time

    import ffmpeg
    import torch
    import whisper

    t0 = time.time()
    with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
        (
            ffmpeg.input(str(audio_filepath))
            .filter("atrim", start=start, end=end)
            .output(f.name)
            .overwrite_output()
            .run(quiet=True)
        )

        use_gpu = torch.cuda.is_available()
        device = "cuda" if use_gpu else "cpu"
        model = whisper.load_model(
            model.name, device=device, download_root=config.MODEL_DIR
        )
        result = model.transcribe(f.name, language="en", fp16=use_gpu)  # type: ignore

    logger.info(
        f"Transcribed segment {start:.2f} to {end:.2f} ({end - start:.2f}s duration) in {time.time() - t0:.2f} seconds."
    )

    # Add back offsets.
    for segment in result["segments"]:
        segment["start"] += start
        segment["end"] += start

    return result


@stub.function(
    image=app_image,
    network_file_systems={config.CACHE_DIR: volume},
    timeout=900,
)
def transcribe_episode(
    audio_filepath: pathlib.Path,
    result_path: pathlib.Path,
    model: config.ModelSpec,
):
    segment_gen = split_silences(str(audio_filepath))

    output_text = ""
    output_segments = []
    for result in transcribe_segment.starmap(
        segment_gen, kwargs=dict(audio_filepath=audio_filepath, model=model)
    ):
        output_text += result["text"]
        output_segments += result["segments"]

    result = {
        "text": output_text,
        "segments": output_segments,
        "language": "en",
    }

    logger.info(f"Writing openai/whisper transcription to {result_path}")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=4)


@stub.function(
    image=app_image,
    network_file_systems={config.CACHE_DIR: volume},
    timeout=900,
)
def process_episode(podcast_id: str, episode_number: str):
    import dacite
    import whisper

    try:
        # pre-download the model to the cache path, because the _download fn is not
        # thread-safe.
        model = config.DEFAULT_MODEL
        whisper._download(whisper._MODELS[model.name], config.MODEL_DIR, False)

        config.RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        config.TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

        metadata_path = get_episode_metadata_path(podcast_id)
        with open(metadata_path, "r") as f:
            data = json.load(f)
            data = data[episode_number]
            logger.info(data)
            episode = dacite.from_dict(
                data_class=podcast.EpisodeMetadata, data=data
            )

        destination_path = config.RAW_AUDIO_DIR / episode.guid_hash
        podcast.store_original_audio(
            url=episode.audio_download_url,
            destination=destination_path,
        )

        logger.info(
            f"Using the {model.name} model which has {model.params} parameters."
        )
        logger.info(f"Wrote episode metadata to {metadata_path}")

        transcription_path = get_transcript_path(episode.guid_hash)
        if transcription_path.exists():
            logger.info(
                f"Transcription already exists for '{episode.title}' with ID {episode.guid_hash}."
            )
            logger.info("Skipping transcription.")
        else:
            transcribe_episode.remote(
                audio_filepath=destination_path,
                result_path=transcription_path,
                model=model,
            )
    finally:
        del stub.in_progress[episode_number]

    return episode


@stub.function(
    image=app_image,
    network_file_systems={config.CACHE_DIR: volume},
)
def fetch_episodes(url: str):
    return podcast.fetch_episodes(url=url)


# @stub.local_entrypoint()
# def search_entrypoint(name: str):
#     # To search for a podcast, run:
#     # modal run app.main --name "search string"
#     for pod in search_podcast.remote(name):
#         print(pod)
