# Implementation Plan: Japanese TTS API with Style-Bert-VITS2

**Branch**: `004-tts-japanese-api` | **Date**: 2025-12-25 | **Spec**: [specs/004-tts-japanese-api/spec.md]
**Input**: Feature specification from `/specs/004-tts-japanese-api/spec.md`

## Summary

This feature implements a high-quality Japanese Text-to-Speech (TTS) service using the `Style-Bert-VITS2` model. The API will provide endpoints for synthesizing natural-sounding speech with fine-grained control over emotions (styles) and voice parameters (speed, pitch). It supports both batch WAV file generation and real-time chunked streaming to minimize perceived latency.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `fastapi`, `style-bert-vits2`, `pydantic`, `python-dotenv`, `prometheus_client`, `pydub`
**Storage**: Local disk for model weights; N/A for transient audio data.
**Testing**: `pytest`, `httpx` (for API testing), `librosa` or `scipy.io.wavfile` (for audio verification).
**Target Platform**: Linux Server (with optional GPU support for faster inference).
**Project Type**: Backend API Service.
**Performance Goals**: < 2.0 seconds for a 20-character sentence (Time to First Byte for streaming).
**Constraints**: Must adhere to the technology stack (FastAPI) and tooling (`uv`, `pydantic`, `ruff`) defined in the constitution.
**Scale/Scope**: Support for at least 2 concurrent synthesis sessions.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Library-First**: The synthesis core will be implemented as a standalone module `src/core/tts`.
- **II. CLI Interface**: A CLI utility `src/cli/tts_cli.py` will be created for local synthesis testing.
- **III. Test-First**: TDD approach using `pytest` to validate parameter parsing and audio header integrity.
- **IV. Integration Testing**: Mock-based and local-integration tests for WebSocket/Streaming endpoints and API Key auth.
- **V. Observability**: Mandatory structured JSON logging for all requests, including character counts and inference time.
- **VI. Semantic Versioning**: Internal API versioning maintained.
- **VII. Simplicity (YAGNI)**: Direct implementation of required parameters without over-abstracting the Style-Bert-VITS2 SDK.
- **Technology Stack and Tooling**: Adheres to Next.js/FastAPI, `uv`, `pydantic`, and `ruff`.

## Project Structure

### Documentation (this feature)

```text
specs/004-tts-japanese-api/
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
├── src/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── tts.py
│   ├── core/
│   │   └── tts/
│   │       ├── model_manager.py  # Model loading and style mapping
│   │       └── synthesizer.py    # Inference logic
│   ├── models/
│   │   └── tts.py                # Pydantic request/response models
│   └── utils/
│       └── audio.py              # WAV formatting and streaming utilities
└── tests/
    └── tts/
        ├── test_api.py
        └── test_synthesis.py
```

**Structure Decision**: Standard FastAPI endpoint structure integrated into the existing backend hierarchy. Core logic isolated in `src/core/tts`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | -          | -                                   |