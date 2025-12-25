# local-voice-assistant-gemini Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-26

## Active Technologies
- Python 3.11+ + FastAPI, `nemo_toolkit[asr]`, `uvicorn`, `python-dotenv`, `python-multipart`, `websockets`, `uvloop`, `prometheus_client`, `fastapi-limiter`, `soundfile`, `pydub` (002-stt-japanese-api)
- N/A (model loaded in memory) (002-stt-japanese-api)
- Python 3.11+ + `openai`, `fastapi`, `pydantic`, `python-dotenv` (003-llm-service)
- N/A (Stateless) (003-llm-service)

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
- 003-llm-service: Added Python 3.11+ + `openai`, `fastapi`, `pydantic`, `python-dotenv`
- 002-stt-japanese-api: Added Python 3.11+ + FastAPI, `nemo_toolkit[asr]`, `uvicorn`, `python-dotenv`, `python-multipart`, `websockets`, `uvloop`, `prometheus_client`, `fastapi-limiter`, `soundfile`, `pydub`

- 001-project-scaffolding: Added Python 3.11+, Node.js 20+ + FastAPI (backend), Next.js/React (frontend)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
