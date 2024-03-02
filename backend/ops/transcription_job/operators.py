import json
import pathlib

from backend.ops.stub import stub
from backend.ops.image import APP_IMAGE
from backend.ops.storage import APP_VOLUME, get_episode_metadata_path, get_podcast_metadata_path, get_transcript_path

from backend.src.podcast.functions.download import store_original_audio
from backend.src.transcription_job.functions.silences import split_silences

from backend.ops.transcription_job.constants import ModelSpec
from backend.src.podcast.types import EpisodeMetadata

from backend.ops import storage
from backend.ops.transcription_job.constants import DEFAULT_MODEL

from backend import _utils; logger = _utils.get_logger(__name__)

@stub.function(
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    cpu=4,
    # gpu="any",
    timeout=600,
)
def transcribe_segment(
    start: float,
    end: float,
    audio_filepath: pathlib.Path,
    model: ModelSpec,
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
            model.name, device=device, download_root=storage.MODEL_DIR
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
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    timeout=900,
)
def transcribe_episode(
    audio_filepath: pathlib.Path,
    result_path: pathlib.Path,
    model: ModelSpec,
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
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    timeout=900,
)
def process_episode(podcast_id: str, episode_number: str):
    import dacite
    import whisper

    try:
        # pre-download the model to the cache path, because the _download fn is not
        # thread-safe.
        model = DEFAULT_MODEL
        whisper._download(whisper._MODELS[model.name], storage.MODEL_DIR, False)

        storage.RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        storage.TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

        metadata_path = get_episode_metadata_path(podcast_id)
        with open(metadata_path, "r") as f:
            data = json.load(f)
            data = data[episode_number]
            logger.info(data)
            episode = EpisodeMetadata(**data)

        destination_path = storage.RAW_AUDIO_DIR / episode.guid_hash
        store_original_audio(
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