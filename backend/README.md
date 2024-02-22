# Refactor
- ui <- api <- ops <- src
    - `api` should only import from `ops`, which in turn should only import from `src` (except for potentially common types which could be hosted elsewhere or cascaded to a types file in each section/directory)
        - `api` should just trigger api functionality via. calling modal stub functions
            - Each route should have its own folder analogous to the url route so it's easy to identify - the same naming should propagate to `ops` and `src` as far as possible to make it easier to know which code calls from where.
        - `ops` should handle just modal functionality & call src code functions
            - All the modal functionality should be wrapped up into classes with the appropriate exit and entry methods for setup and teardown. Common functionality can be placed in a `_utils` folder for eg.
        - `src` should host the core logic which can also be utilised elsewhere or locally - enabling local testing etc.
            - Instead of separate functions the `src` folder per functionality type should have a class that groups all the functionality eg. `PodcastPresenter`. Common functionality can be placed in a `_utils` folder for eg.

# UI 
- Want a button on each podcast page `transcribe this episode` which doesn't open up a new page but hits an end-point on fast-api eg. `/api/transcribe/{episode_number}` and then has a loading spinner which runs whilst transcribing, at the end it presents the transcription
- Want a way for the user to enter in their credentials via. the UI and for this to be stored safely and accessible on the backend, but until there is a better concept of user can leave this - it may turn out we want to just use a service account for all model credentials etc. and so don't need anything from the user

# Known Issues
- The file storage volume may get corrupt if the data stored doesn't conform to expectation & thus can't be parsed as expected etc., in such a situation you will get obtuse errors that make it seem like a http/frontend issue
    - To troubleshoot this - just delete the file storage volume
    - To avoid this & fix - create dataclasses/pydantic validators for all the data being stored and wrap the storage and retrieval steps in try/except statements with error logging (write to a file location what was stored etc. for troubleshooting)

- If the infrastructure fails in the middle of a transcription_job then there is no mechanism for picking it back up again. The poll status tells you the job is incomplete but there is no mechanism to restart and complete the job from the incomplete status. Might want to write a modal operator that intermittently checks the status of any jobs (or just on startup) and picks them back up somehow if incomplete