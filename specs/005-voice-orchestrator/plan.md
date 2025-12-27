# Implementation Plan: Voice Interaction Orchestrator

**Branch**: `005-voice-orchestrator` | **Date**: 2025-12-27 | **Spec**: [/specs/005-voice-orchestrator/spec.md]
**Input**: Feature specification from `/specs/005-voice-orchestrator/spec.md`

## Summary

Implement a real-time voice interaction orchestrator that chains Speech-to-Text (STT), Large Language Model (LLM), and Text-to-Speech (TTS) services. The orchestrator will expose a WebSocket endpoint for low-latency, multi-turn, and streaming communication, supporting user "barge-in" by canceling ongoing generations when new speech is detected.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, websockets, pydantic, (existing STT, LLM, TTS modules)  
**Storage**: In-memory (Session-bound) for conversation history.  
**Testing**: pytest  
**Target Platform**: Linux server  
**Project Type**: Web application (Backend)  
**Performance Goals**: Time to First Audio Byte (TTFB) < 3 seconds  
**Constraints**: 16kHz, 16-bit PCM (Mono) audio format; interleaved JSON (Text) and Audio (Binary) frames.  
**Scale/Scope**: Real-time multi-turn voice session management.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Library-First**: The orchestration core will be implemented in `src/core/orchestrator`.
- **II. CLI Interface**: A CLI test utility `src/cli/orchestrate_test.py` will be created.
- **III. Test-First**: TDD approach using pytest in `tests/orchestrator`.
- **IV. Integration Testing**: End-to-end integration tests for the STT -> LLM -> TTS chain.
- **V. Observability**: Structured JSON logging for session IDs, stage latencies, and total turn duration.
- **VI. Semantic Versioning**: Standard internal versioning.
- **VII. Simplicity (YAGNI)**: Minimal in-memory session management without persistent DB overhead.
- **Technology Stack and Tooling**: Adheres to FastAPI, `uv`, `pydantic`, and `ruff`.

## Project Structure

### Documentation (this feature)

```text
specs/005-voice-orchestrator/
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
│   │           └── orchestrator.py  # WebSocket endpoint
│   ├── core/
│   │   └── orchestrator/
│   │       ├── session.py           # Session context and history
│   │       └── processor.py         # Pipeline orchestration logic
│   └── cli/
│       └── orchestrate_test.py      # Local testing CLI
└── tests/
    └── orchestrator/
        ├── test_session.py
        ├── test_processor.py
        └── test_integration.py
```

**Structure Decision**: Option 2 (Web application) since it integrates into the existing FastAPI backend and requires WebSocket handling.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | -          | -                                   |