from fastapi import FastAPI
from backend.api.podcast.routes import PODCAST_ROUTER
from backend.api.transcription_job.routes import TRANSCRIPTION_ROUTER

web_app = FastAPI()
web_app.include_router(PODCAST_ROUTER)
web_app.include_router(TRANSCRIPTION_ROUTER)