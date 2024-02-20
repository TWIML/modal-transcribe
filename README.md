# Modal Transcribe

This is an adaptation of Modal's Whisper transcription example [[blog](https://modal.com/docs/examples/whisper-transcriber), [github](https://github.com/modal-labs/modal-examples/tree/main/06_gpu_and_ml/openai_whisper/pod_transcriber)].
Key changes:
- eliminated podcast search; hardcoded for TWIML
- replaced react front end with sveltekit/tailwind

## Getting Started

1. Clone the repo
  
2. Create a Modal Account

Visit [modal.com](https://modal.com) and sign up.

3. Install Modal CLI

```
pip install modal     # Note: Requires Python 3.11.x
```

```
python3 -m modal setup     # this will open a web page allowing you to create a token to authorize your client
```

4. Build the Front End

cd into the frontend directory, and run:

```
npm install
npx vite build --watch
```

The last command will start a watcher process that will rebuild your static frontend files whenever you make changes to the frontend code.

5. Deploy to Modal

Once you have vite build running, in a separate shell run this to start an ephemeral/dev app on Modal:

```
modal serve backend.main
```

The modal app will print two URLs in its shell window. Open the one that looks like this to access the front end:
    Created fastapi_app => https://sbc--whisper-pod-transcriber-fastapi-app-dev.modal.run

The other URL is the modal admin/back end, which looks like this:
    View app at https://modal.com/sbc/apps/ap-hkENjVd3K2PDbPtuwoWKND

Pressing Ctrl+C will stop your app.



