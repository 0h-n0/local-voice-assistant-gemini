# Local Voice Assistant - Project Scaffolding

This repository contains the basic project structure for a local voice assistant, including a FastAPI backend and a Next.js (TypeScript) frontend.

## Quickstart

This guide provides the steps to get the backend and frontend servers running.

### Prerequisites

- Python 3.11+
- Node.js 20+
- `uv` (Python package installer)
- `npm` or `yarn` (Node.js package manager)
- Docker (for Redis)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone git@github.com:0h-n0/local-voice-assistant-gemini.git
    cd local-voice-assistant-gemini
    ```

2.  **Install Backend Dependencies**:
    Navigate to the `backend` directory, create a virtual environment, and use `uv` to install the packages.
    ```bash
    cd backend
    uv venv --python 3.11
    . .venv/bin/activate
    uv pip install -r requirements.in
    ```

3.  **Install Frontend Dependencies**:
    Navigate to the `frontend` directory and use `npm` or `yarn`.
    ```bash
    cd ../frontend
    npm install
    # or yarn install
    ```

### Running the Application

1.  **Start Redis (for Rate Limiting)**:
    ```bash
    docker run -d --name redis-rate-limiter -p 6379:6379 redis
    ```

2.  **Configure API Key**:
    Create a `.env` file in the `backend/` directory:
    ```
    API_KEY="your_secret_api_key_here"
    ```

3.  **Start the Backend Server**:
    From the `backend` directory (ensure your virtual environment is active):
    ```bash
    . .venv/bin/activate
    uvicorn src.main:app --reload
    ```
    The server will be running at `http://127.0.0.1:8000`. You can check the health status by visiting `http://127.0.0.1:8000/health`.

4.  **Start the Frontend Server**:
    From the `frontend` directory:
    ```bash
    npm run dev
    # or yarn dev
    ```
    The frontend development server will be running at `http://localhost:3000`.

You should now see the placeholder "Local Voice Assistant" page in your browser.

## Japanese STT API

The backend includes a Japanese Speech-to-Text (STT) API using `reazon-research/reazonspeech-nemo-v2`.

### Transcribe Audio File

Send a POST request to `/api/v1/transcribe/file` with an audio file (WAV or MP3, max 50MB).

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/transcribe/file" \
     -H "X-API-Key: your_secret_api_key_here" \
     -H "Content-Type: multipart/form-data" \
     -F "audio_file=@path/to/your/audio.wav;type=audio/wav"
```

### Transcribe Live Audio Stream

Connect to the WebSocket at `/api/v1/transcribe/stream` and stream raw audio data.

```bash
# Using websocat
websocat "ws://127.0.0.1:8000/api/v1/transcribe/stream?api_key=your_secret_api_key_here"
```

## Linting and Quality Checks

To run the project's linters for both backend and frontend from the root directory:

```bash
npm run lint
```