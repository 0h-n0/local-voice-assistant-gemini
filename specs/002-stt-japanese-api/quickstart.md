# Quickstart: Japanese STT API

This guide provides the steps to set up and interact with the Japanese Speech-to-Text API.

## Prerequisites

- Python 3.11+
- `uv` (Python package installer)
- Docker (for `fastapi-limiter` Redis backend, if used)
- A valid API Key (to be provided separately)

## Setup

1.  **Clone the repository**:
    ```bash
    git clone git@github.com:0h-n0/local-voice-assistant-gemini.git
    cd local-voice-assistant-gemini
    ```

2.  **Create a virtual environment and install dependencies**:
    ```bash
    cd backend
    uv venv
    . .venv/bin/activate
    uv pip install -r requirements.in # This will include nemo_toolkit[asr]
    ```
    _Note: The `nemo_toolkit[asr]` installation can be substantial and may take some time._

3.  **Download the STT model**:
The `reazonspeech-nemo-v2` model will need to be downloaded. This typically happens on first use or can be pre-downloaded. Refer to the model's documentation for exact steps or the API's setup script.

4.  **Configure API Key**:
Create a `.env` file in the `backend/` directory with your API Key:
    ```
    API_KEY="your_secret_api_key_here"
    ```

5.  **Start Redis (for rate limiting)**:
If `fastapi-limiter` is configured with Redis, start a Redis instance (e.g., via Docker):
    ```bash
    docker run -d --name redis-rate-limiter -p 6379:6379 redis
    ```

## Running the API

From the `backend/` directory (with virtual environment activated):

```bash
uvicorn src.main:app --reload
```
The API will be running at `http://127.0.0.1:8000`. The OpenAPI documentation will be available at `http://127.0.0.1:8000/docs`.

## Interacting with the API

### Transcribe File (`/transcribe/file`)

Use `curl` or a similar HTTP client. Replace `path/to/your/audio.wav` and `YOUR_API_KEY`.

```bash
curl -X POST "http://127.0.0.1:8000/transcribe/file" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@path/to/your/audio.wav;type=audio/wav"
```

### Transcribe Stream (`/transcribe/stream`)

This endpoint uses WebSockets. You will need a WebSocket client. Example usage with `websocat` (install via `cargo install websocat`):

```bash
# Connect to the WebSocket
websocat "ws://127.0.0.1:8000/transcribe/stream?api_key=YOUR_API_KEY"
```
Once connected, stream raw audio data (e.g., 16kHz, mono, 16-bit PCM) into the WebSocket. The API will return JSON transcription results.

```