# Notes

## Refactor

- ui <- api <- ops <- src
  - `api` should only import from `ops`, which in turn should only import from `src` (except for potentially common types which could be hosted elsewhere or cascaded to a types file in each section/directory)
  - `api` should just trigger api functionality via. calling modal stub functions
    - Each route should have its own folder analogous to the url route so it's easy to identify - the same naming should propagate to `ops` and `src` as far as possible to make it easier to know which code calls from where.
  - `ops` should handle just modal functionality & call src code functions
    - All the modal functionality should be wrapped up into classes with the appropriate exit and entry methods for setup and teardown. Common functionality can be placed in a `_utils` folder for eg.
  - `src` should host the core logic which can also be utilised elsewhere or locally - enabling local testing etc.
    - Instead of separate functions the `src` folder per functionality type should have a class that groups all the functionality eg. `PodcastPresenter`. Common functionality can be placed in a `_utils` folder for eg.

## Debugging

- You can use `modal nfs ...` to interact with the storage volume, `modal shell ...` to open up a shell on modal (not the one our app is running in), and `modal container ...` to interact with the apps container but in a very limited/obfuscated manner

## UI 

- Want a button on each podcast page `transcribe this episode` which doesn't open up a new page but hits an end-point on fast-api eg. `/api/transcribe/{episode_number}` and then has a loading spinner which runs whilst transcribing, at the end it presents the transcription
- Want a way for the user to enter in their credentials via. the UI and for this to be stored safely and accessible on the backend, but until there is a better concept of user can leave this - it may turn out we want to just use a service account for all model credentials etc. and so don't need anything from the user

## Known Issues

- The file storage volume may get corrupt if the data stored doesn't conform to expectation & thus can't be parsed as expected etc., in such a situation you will get obtuse errors that make it seem like a http/frontend issue
  - To troubleshoot this - just delete the file storage volume
  - To avoid this & fix - create dataclasses/pydantic validators for all the data being stored and wrap the storage and retrieval steps in try/except statements with error logging (write to a file location what was stored etc. for troubleshooting)

- If the infrastructure fails in the middle of a transcription_job then there is no mechanism for picking it back up again. The poll status tells you the job is incomplete but there is no mechanism to restart and complete the job from the incomplete status. Might want to write a modal operator that intermittently checks the status of any jobs (or just on startup) and picks them back up somehow if incomplete

- Was getting many pydantic errors due to the originally installed version on the modal image using pip being out of date, and even when re-installing a later version specifically it reverted somehow to an old version it appears. So am trialling writing all dependencies to a lock file via. poetry and installing from there - added benefit is anybody installing the repo and testing locally can have access to the same setup as the image (they will have to sort the linux installs though)
  - Had an associated issue when moving to using a `poetry.lock` file for *libcublas[0-9] not found* or somethin, fixed it by fixing the torch version to be used as [here](https://stackoverflow.com/questions/76327419/valueerror-libcublas-so-0-9-not-found-in-the-system-path)
  - However it is a lot slower to startup when using poetry.lock as the installation method, it seems like it needs to upload local files each and every time which is tedious
- Warnings from pytorch regards pyannote and whisper and transformer libs calls to it - using deprecated functions etc. not sure of fix for now (whether to suppress or try to correct since it is coming from the internal libs not our usage of them)

- It needs a lot more error handling and try/except statements and debugging, for example a common error is if data isn't written to file properly and silent fails, then whenever trying to access the api/urls you just get 500 server errors which don't specify anything, so need to wrap writing to files in try/excepts etc. and ensure type hinting everywhere and data validation to ensure data is being moved around as intended

- If you get exceptionally long load and mount times - my issue was I had a .venv folder of 5.5GB in the backend dir and it was trying to mount that, so I need to find a way to determine how to do a .gitignore on the mount kind of thing - for now I removed the .venv
  - I would like to create a .venv on modal only not local, that would be best

- Some settings are hardcoded when they should really be sent through, need to think how to do (eg. whisper model ... or maybe it needs to be in another config space)
