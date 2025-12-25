# Implementation Plan: Japanese STT API with ReazonSpeech

**Branch**: `002-stt-japanese-api` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-stt-japanese-api/spec.md`

## Summary

This plan outlines the implementation of a Japanese Speech-to-Text (STT) API using `reazon-research/reazonspeech-nemo-v2`. The API will provide endpoints for transcribing audio files and live microphone input, incorporating API key authentication, basic rate limiting, and observability features.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, `nemo_toolkit[asr]`, `uvicorn`, `python-dotenv`, `python-multipart`, `websockets`, `uvloop`, `prometheus_client`, `fastapi-limiter`, `soundfile`, `pydub`
**Storage**: N/A (model loaded in memory)
**Testing**: `pytest`, `httpx`
**Target Platform**: Linux Server
**Project Type**: Backend API
**Performance Goals**: As per SC-001 (5s for 30s audio), SC-002 (500ms latency for streaming)
**Constraints**: Must adhere to the technology stack (FastAPI) and tooling (`uv`, `pydantic`, `ruff`) defined in the constitution. Model: `reazon-research/reazonspeech-nemo-v2`.
**Scale/Scope**: Initial implementation handles up to 5 concurrent file requests and continuous streaming for 1 hour.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Library-First**: Does the feature start as a self-contained library? - Yes, the STT API will be a self-contained module within the backend.
- **II. CLI Interface**: Does the library expose its functionality via a CLI? - The primary interface is an API, but internal components can expose CLI for testing/debugging.
- **III. Test-First**: Are tests written before the implementation? - Yes, all API endpoints and core logic will be test-driven.
- **IV. Integration Testing**: Are integration tests planned for critical pathways? - Yes, for API key authentication, rate limiting, and the STT transcription process (file and streaming).
- **V. Observability**: Is structured logging included in the plan? - Yes, structured logging for API events and Prometheus metrics are required (FR-010, FR-011).
- **VI. Semantic Versioning**: Is the versioning scheme clear for any new or updated APIs/packages? - Yes, API versioning will follow project guidelines.
- **VII. Simplicity (YAGNI)**: Is the proposed solution the simplest possible way to meet requirements? - Yes, focusing on the core STT functionality and specified non-functional requirements.
- **Technology Stack and Tooling**: Does the project adhere to the specified technology stack (Next.js/FastAPI) and tooling (`uv`, `pydantic`, `ruff`)? - Yes, backend uses FastAPI, `uv`, `pydantic`, `ruff`.

## Project Structure

### Documentation (this feature)

```text
specs/002-stt-japanese-api/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
└── src/
    ├── api/
    │   ├── v1/
    │   │   ├── endpoints/
    │   │   │   ├── stt.py
    │   │   │   └── health.py (existing, if any)
    │   │   └── dependencies.py (for API Key auth)
    │   ├── main.py (existing)
    │   └── models/
    │       └── stt_models.py
    ├── core/
    │   └── stt_processor.py (handles Nemo model interaction)
    ├── middlewares/
    │   ├── rate_limiter.py
    │   └── logging.py
    └── utils/
        └── audio_utils.py (audio format conversion, chunking)
```

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | - | - |