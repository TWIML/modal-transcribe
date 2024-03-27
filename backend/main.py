"""
Assuming execution via. `modal serve backend.main` then this file is the entry point to the whole application
    1. It spins up the modal resources according to what is discoverable here thus you must import all modal operators (@stub.functions etc.) here else the modal client cannot see them
    2. Since you run `modal serve` it looks for the @asgi_app to spin up the web-server, you must mount the frontend build files here to serve the frontend. These should be in `frontend/dist` & get created upon `npm install; npx vite build --watch` in the frontend
    3. To make all the api routes available you must import the routers for them here and then include them in the web_app instance
"""

import fastapi.staticfiles
from modal import Mount, asgi_app

from backend.ops.stub import stub
from backend.ops.storage import APP_VOLUME
from backend.ops.image import APP_IMAGE
from backend.ops import storage

# DISCOVERS MODAL FUNCTIONALITY FROM HERE
from backend.ops.diarised_transcribe.operators import *
from backend.ops.podcast.operators import *

from backend.api.podcast.routes import PODCAST_ROUTER
from backend.api.diarised_transcribe.routes import DIARISED_TRANSCRIBE_ROUTER

from fastapi import FastAPI

##################
# NOTE: Adding routers to the web-app, may be best to make this auto-discovered eventually
# NOTE: If not added here you'll get `405 Method Not Allowed` errors which can be obtuse
# ... so maybe want to add some custom error handling for the API routers in a common
# api functions folder eg. `_utils/errors` etc.
web_app = FastAPI()
web_app.include_router(PODCAST_ROUTER)
web_app.include_router(DIARISED_TRANSCRIBE_ROUTER)
############################################


############################################


@stub.function(
    mounts=[Mount.from_local_dir(
        storage.ASSETS_PATH, # local `frontend/dist` path - compiled frontend code
        remote_path="/assets" # modal `/assets` path
    )],
    network_file_systems={storage.CACHE_DIR: APP_VOLUME},
    timeout=6_000,  # 100mins - NOTE: ...necessary to prevent subtask timeouts?
    keep_warm=2,
)
@asgi_app()
def fastapi_app():
    web_app.mount(
        "/", # root url on website
        fastapi.staticfiles.StaticFiles(directory="/assets", html=True) # modal `/assets` path
    )
    return web_app
