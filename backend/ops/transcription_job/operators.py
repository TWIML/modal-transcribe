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
            episode = dacite.from_dict(
                data_class=EpisodeMetadata, data=data
            )

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

############################################################
# NOTE: Functions being worked on in the interim as html/svelte
# is not working properly so can't effectively refactor the rest
# of the codebase, will need to do together to restructure, remove
# unused funcs, rename and resituate files, funcs, config etc.
############################################################

# download step
# NOTE: if this is not a stub/modal-func, and not called with .remote - does it happen on my local machine?
# ... or if the parent func calling it is a modal stub/func and is called with .remote does that behaviour propagate
# downwards and so this would be executed remotely supposing its parent is (& it also gets all the image/volume settings
# from its paent too?)
def download_step(fixed_podcast_url): # 1st step
    # download step
    import urllib
    from backend.src.podcast.types import DownloadResult
    from backend.src.podcast.functions import sizeof_fmt
    request = urllib.request.Request(
        fixed_podcast_url,
        data=None,
        # Set a user agent to avoid 403 response from some podcast audio servers.
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        },
    )
    response = urllib.request.urlopen(request)
    podcast_download_result = DownloadResult(
        data=response.read(),
        content_type=response.headers["content-type"],
    )
    # storing the audio intermediately
    storage.RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True) # must create directory on remote
    audio_downloaded_path = storage.RAW_AUDIO_DIR / "fixed_podcast_audio"
    humanized_bytes_str = sizeof_fmt(num=len(podcast_download_result.data))
    size_of_download_msg = f"Downloaded {humanized_bytes_str} episode from URL."
    logger.info(size_of_download_msg)
    with open(audio_downloaded_path, "wb") as f:
        f.write(podcast_download_result.data)
    audio_file_storage_location_msg = f"Stored audio episode at {audio_downloaded_path}."
    logger.info(audio_file_storage_location_msg)
    msgs = {
        'size_msg': size_of_download_msg, 
        'audio_stored_msg': audio_file_storage_location_msg
    }
    return audio_downloaded_path, msgs

@stub.function(
    image=APP_IMAGE,
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    timeout=6000,
    retries=10 # 100mins
)
def download_transcribe_annotate_fixed_podcast_in_single_job_process(fixed_podcast_url: str):
    '''
    Hardcoded function for testing process whilst waiting to discuss
    cleaning up codebase and refactoring +  getting some guidance on
    frontend stuff

    This will download the podcast to a location, transcribe it,
    store the transcript, and then also diarize the podcast,
    annotate the transcription with diarisation, re-store
    and the provide the path/url to see them
    '''
    (
        audio_downloaded_path, # Path object
        download_step_msgs
    ) = download_step(fixed_podcast_url)

    # transcribe step
    import tempfile
    import torch
    import whisper
    import time

    # whisper set up
    models_list = whisper.available_models() # the models you have access to
    use_gpu = torch.cuda.is_available() # if gpu is available or not (won't be locally for me - needs special cuda drivers etc. and i haven't set up)
    device = 'cuda' if use_gpu else 'cpu' # will be 'cpu' for me, see above comment
    # whisper model
    modelname = 'base.en' # (74M params)
    model = whisper.load_model(
        name=modelname, 
        device=device
    )
    # transcribing
    t0 = time.time()
    transcription = model.transcribe(
        audio=str(audio_downloaded_path), 
        language='en', 
        fp16=use_gpu # floating point precision
    )
    transcribe_time_taken_msg = f'Transcription took: {time.time() - t0:.2f} seconds'
    logger.info(transcribe_time_taken_msg)

    # storing the transcription
    storage.TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)
    transcription_storage_path = storage.TRANSCRIPTIONS_DIR / "fixed_podcast_transcript"
    with open(transcription_storage_path, "w") as f:
        json.dump(transcription, f, indent=4)
    transcript_json_storage_location_msg = f"Stored transcript at {transcription_storage_path}."
    logger.info(transcript_json_storage_location_msg)

    return download_step_msgs, transcript_json_storage_location_msg, transcription