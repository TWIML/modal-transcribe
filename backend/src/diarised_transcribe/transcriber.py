import whisper, pathlib, time, tempfile, torch, ffmpeg

from typing import Iterator
from backend.src.diarised_transcribe.types import DiarisedSegmentBounds, TranscriptionResult, TranscriptionNestedSegment

from backend._utils import get_logger; logger = get_logger(__name__)

class WhisperTranscriber:

    def __init__(self):
        pass

    @staticmethod
    def download_model_to_path(
        model_name: str, 
        model_dir: pathlib.Path, 
        in_memory: bool
    ) -> None:
        whisper._download(
            url=whisper._MODELS[model_name],
            root=model_dir,
            in_memory=in_memory,
        )
    
    @staticmethod
    def transcribe_segment(
        diarised_segment_bounds: DiarisedSegmentBounds,
        audio_file_path: pathlib.Path,
        model_name: str,
        model_dir: pathlib.Path
    ) -> TranscriptionResult:
        '''
        Transcribes the diarised segment i.e. a contiguous segment
        identified as an utterance of a single speaker

        NOTE: does not fully follow Mochan's approach as uses ffmpeg
        to get the audio segment, Mochan uses torch itself to index the
        audio file
        '''

        print(f"""
            ---------------------------HITTING THE TRANSCRIBER------------------------
              
            This is the audio path: {audio_file_path}
            This is the model name: {model_name}
            This is the model dir: {model_dir}
        """)

        t0 = time.time()

        # Trimming the audio file to the diarised segment bounds
        start, end, speaker = (
            diarised_segment_bounds.start,  
            diarised_segment_bounds.end,
            diarised_segment_bounds.speaker
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
            (
                ffmpeg.input(str(audio_file_path))
                .filter("atrim", start=start, end=end)
                .output(f.name)
                .overwrite_output()
                .run(quiet=True)
            )

            # Loading the model from disk
            use_gpu = torch.cuda.is_available()
            device = "cuda" if use_gpu else "cpu"
            model = whisper.load_model(
                model_name, 
                device=device, 
                download_root=model_dir
            )

            # Transcribing the audio
            unparsed_result: dict = model.transcribe(
                f.name, 
                language="en", # BUG: shouldn't hardcode the language - state in a config.yaml for the model on root level of repo or something
                fp16=use_gpu
            )  # type: ignore
            for _ in unparsed_result:
                print(f'{_} : \n\t {unparsed_result[_]}')

        # Logging time taken for transcription
        logger.info(
            f"Transcribed segment {start:.2f} to {end:.2f} ({end - start:.2f}s duration) in {time.time() - t0:.2f} seconds."
        )

        # Unpacking the result into typed structure
        transcription_result = TranscriptionResult(
            text=unparsed_result['text'],
            segments=unparsed_result['segments'],
            language=unparsed_result['language'],
            speaker=speaker
        )

        # Adding back the start and end offsets
        for segment in transcription_result.segments:
            segment.start += start
            segment.end += start

        return transcription_result       

    