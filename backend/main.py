from modal import Mount, asgi_app

from backend.ops.stub import stub
from backend.ops.storage import APP_VOLUME
from backend import config

# think you must import all modal operator functions here (might want to create a class that discovers them, as long as in files of same name in each api subdirectory)

from backend.ops.podcast.operators import * # could also be in podcast folder you use __init__.py to import all operators into there, and then here you just import the podcast package/folder (but long term best to make them auto-discoverable)
from backend.ops.transcription_job.operators import *


@stub.function(
    mounts=[Mount.from_local_dir(config.ASSETS_PATH, remote_path="/assets")],
    network_file_systems={config.CACHE_DIR: APP_VOLUME},
    timeout=6_000, # 100mins - NOTE: ...necessary to prevent subtask timeouts?
    keep_warm=2,
)
@asgi_app()
def fastapi_app():
    import fastapi.staticfiles
    from backend.api.main import web_app 
    # NOTE: this import is what makes all the routes in `api` available to the modal frontend
    web_app.mount(
        "/", fastapi.staticfiles.StaticFiles(directory="/assets", html=True)
    )
    return web_app