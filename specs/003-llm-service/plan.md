# Implementation Plan: OpenAI LLM Service

**Branch**: `003-llm-service` | **Date**: 2025-12-25 | **Spec**: [specs/003-llm-service/spec.md]
**Input**: Feature specification from `/specs/003-llm-service/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements an interface to OpenAI's `gpt-5-mini` model, supporting multi-turn chat history, batch and streaming (SSE) response modes, and structured JSON logging for token usage tracking.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `openai`, `fastapi`, `pydantic`, `python-dotenv`
**Storage**: N/A (Stateless)
**Testing**: `pytest`, `pytest-asyncio`, `respx`
**Target Platform**: Linux (Docker)
**Project Type**: Backend service
**Performance Goals**: < 3s for non-streaming requests.
**Constraints**: Requires `OPENAI_API_KEY` in environment. Model: `gpt-5-mini`.
**Scale/Scope**: Initial implementation for single-assistant use.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Library-First**: Core logic will be in `src/core/llm`.
- **II. CLI Interface**: Test CLI provided in `src/cli/llm_test.py`.
- **III. Test-First**: TDD with `pytest` and `respx` for API simulation.
- **IV. Integration Testing**: Mocked integration tests for all response modes.
- **V. Observability**: Structured JSON logging for token tracking.
- **VI. Semantic Versioning**: N/A (Internal).
- **VII. Simplicity (YAGNI)**: Minimal OpenAI SDK wrapper.
- **Technology Stack and Tooling**: Adheres to FastAPI, `uv`, `pydantic`, and `ruff`.

## Project Structure

### Documentation (this feature)

```text
specs/003-llm-service/
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
│   │           └── llm.py
│   ├── core/
│   │   └── llm/
│   │       ├── client.py
│   │       └── service.py
│   ├── models/
│   │   └── llm.py
│   └── utils/
│       └── logging.py
└── tests/
    └── integration/
        └── test_llm.py
```

**Structure Decision**: Integrated into existing `backend/` structure as a core service.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | -          | -                                   |