import whisper, pathlib

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

    