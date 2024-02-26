from modal import Image
from backend import backend_root_module_directory as rootdir

APP_IMAGE = (
    Image.debian_slim()
    .apt_install("git")
    .poetry_install_from_file(
        poetry_pyproject_toml=f'{rootdir}/pyproject.toml',
        poetry_lockfile=f'{rootdir}/poetry.lock',
        ignore_lockfile=False
    )
    # .pip_install(
    #     "git+https://github.com/openai/whisper.git",
    #     "dacite",
    #     "jiwer",
    #     "ffmpeg-python",
    #     "gql[all]~=3.0.0a5",
    #     "pandas",
    #     "loguru==0.6.0",
    #     "torchaudio==2.1.0",
    #     "pyannote.audio",
    #     "fastapi==0.110.0",
    #     "pydantic==2.6.2"
    # )
    .apt_install("ffmpeg") # NOTE: can move up to initial .apt_install ?
    .pip_install("ffmpeg-python") # NOTE: can remove, already done in poetry.lock ?
)