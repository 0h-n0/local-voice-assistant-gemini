# local-voice-assistant-gemini Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-26

## Active Technologies
- Python 3.11+ + FastAPI, `nemo_toolkit[asr]`, `uvicorn`, `python-dotenv`, `python-multipart`, `websockets`, `uvloop`, `prometheus_client`, `fastapi-limiter`, `soundfile`, `pydub` (002-stt-japanese-api)
- N/A (model loaded in memory) (002-stt-japanese-api)
- Python 3.11+ + `openai`, `fastapi`, `pydantic`, `python-dotenv` (003-llm-service)
- N/A (Stateless) (003-llm-service)
- Python 3.11+ + `fastapi`, `style-bert-vits2`, `pydantic`, `python-dotenv`, `prometheus_client`, `pydub` (004-tts-japanese-api)
- Local disk for model weights; N/A for transient audio data. (004-tts-japanese-api)
- Python 3.11+ + FastAPI, websockets, pydantic, (existing STT, LLM, TTS modules) (005-voice-orchestrator)
- In-memory (Session-bound) for conversation history. (005-voice-orchestrator)

- Python 3.11+, Node.js 20+ + FastAPI (backend), Next.js/React (frontend) (001-project-scaffolding)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11+, Node.js 20+: Follow standard conventions

## Recent Changes
- 005-voice-orchestrator: Added Python 3.11+ + FastAPI, websockets, pydantic, (existing STT, LLM, TTS modules)
- 004-tts-japanese-api: Added Python 3.11+ + `fastapi`, `style-bert-vits2`, `pydantic`, `python-dotenv`, `prometheus_client`, `pydub`
- 003-llm-service: Added Python 3.11+ + `openai`, `fastapi`, `pydantic`, `python-dotenv`


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
