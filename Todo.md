# Next Steps
1. Comparing the output of your code with Mochan's in terms of transcription and diarization performance
    - there are examples on google-drive, transcribe the same podcast episode and compare
2. Ensure we're creating all the output files we need for downstream tasks
    - To replicate outputs from mochan's pipeline that are consumed by the rag codebase embedding pipeline e.g. json, md etc. (examples of these will be on the google drive)
3. Figure out the right storage strategy for the project. Not sure GDrive or Modal are the right option (but not sure neither aren't either) but in any case probably should have just one.
    - Use S3 for the modal frontend (first class auto-write behaviour) - https://modal.com/docs/guide/cloud-bucket-mounts
        - Only allow 'official' writes to it by storing the keys in a local .env file
4. Figure out how to íntegrate the pipeline parts (who puts/looks for what files where)
    - Solved if step 2 done correctly BUT work still remains from embedding pipeline step to pull the transcripts in
5. A catch-up mode for the modal pipeline that transcribes all episodes with missing transcriptions
    - Scan the feed of podcasts, check which are already transcribed, then transcribe those which are not yet done
        - ISSUE: Might be too expensive to trial out on modal free plan, so best could be check logic works & leave it till deployment to try there
6. Testing and documenting how to run the pipeline locally and on modal
    - Example notebook for how to run without modal (e.g. import into nb the podcast feed downloader, how to select one to download locally, and then running the diarisation, transcription step)
    - Make the src execution have an easy single entry point (like the ops `trigger_process` but won't have all the modal distributed or gpu functionality etc.)
7. Write up README or another MD file to make onboarding and contributing easier
    - Explaining architecture and how to use, and how to set model-config if they want to use on different settings etc.
8. Allowing user to swap out params like model (already there but V3 not on list) and quantization, and perhaps compare results
    - So change the class interface to also enable people, when running in nbs, to be able to pass their own parameters for the model
9. Optimising/speeding up file storage and model downloads etc.
10. Evaluation of outputs from transcription (see point 1.)


-----------

# Steps

1. Clean up and finalise what's been done so far
2. File restructure as below
3. README and point 6. above (enable work in nb)
4. Exceptions and error-handling to make more robust
5. Storing to S3
6. Any speed ups as above point 9.
*. **You removed the background jobs to enable processes to run in the bgd, you need to put that back**

fetch('api/transcribe/623') ---------------------HICCOUGH THEN FAIL OR IF NO HICCOUGH THEN-----------> DONE
fetch('api/transcribe/623') -> TRIGGER A JOB, THEN JOB HAPPENS ASYNC REGARDLESS OF INTERRUPTIONS ----> BGD

-----------

# File Restructure

__common__
    src/
        ???
    ops/
        APP_IMAGE
        APP_VOLUME
        MODAL_EXCEPTION_MSGS
    api/
        FASTAPI_SETTINGS
    model_config.yml

podcasts/
    src.py
    ops.py -> 
    api.py
diarised_transcribe/
    src.py
    ops.py -> WRITE, EXECUTION, EXCEPTION_MSG(path/filename)
    api.py

... -> WRITE TO STORAGE FOR THE EMBEDDING PIPELINE TO USE, OR ENABLE HUMAN TO DOWNLOAD TRANSCRIPT

-------------

# User & Use Case

[Users will be running locally individually, & eventually a small production version for select people using (twiml staff etc.)]

At the moment (browse and look and ui button interaction)
- It is a display of all episodes published, and gives a way to view their individual details inc. transcripts
- User triggers transcription via. clicking button on UI - only for episodes that have been published

Original intention (practical single use interface) - STILL NEEDED (CAN COMBINE WITH ABOVE, SEE C1 BELOW)
- A plain website just with a button to upload a file, and then it transcribes and triggers an automatic download in the browser

Possible paths
- Experimentation platform

*C1: to make this work you, whilst allowing that transcription to then be associated on the ui with the episode once it is published, you would need the hashing method used on the published episode to match with the hash generated on user upload of audio (which would need some thought - some way to use the same name or episode title for the hash)

--------------

# Goal

Make sure all transcripts are available for RAG experiments
Make available for uploading to twiml website

--------------

# Collaborating on the repo

- Sam working on frontend so no overlap
- 
