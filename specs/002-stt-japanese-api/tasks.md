# Tasks: Japanese STT API with ReazonSpeech

**Input**: Design documents from `/specs/002-stt-japanese-api/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: All API endpoints and core logic will be test-driven.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description with file path`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the environment and basic project structure for the STT API.

- [x] T001 Create `backend/src/api/v1/endpoints/` directory.
- [x] T002 Create `backend/src/core/` directory.
- [x] T003 Create `backend/src/middlewares/` directory.
- [x] T004 Create `backend/src/utils/` directory.
- [x] T005 Update `backend/requirements.in` with `nemo_toolkit[asr]`, `python-multipart`, `websockets`, `uvloop`, `prometheus_client`, `fastapi-limiter`, `soundfile`, `pydub`, `python-json-logger`.
- [x] T006 [P] Install `nemo_toolkit[asr]` and other updated backend dependencies (`cd backend && uv pip install -r requirements.in`).
- [x] T007 [P] Update `backend/src/main.py` to import necessary middleware and initialize FastAPI with the updated `main.py` from the previous feature.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement core infrastructure components that all STT API endpoints will rely on.

- [x] T008 [P] Implement API Key authentication dependency in `backend/src/api/v1/dependencies.py`.
- [x] T009 [P] Create `backend/src/models/stt_models.py` with Pydantic models for `AudioInput` and `TranscriptionResult`.
- [x] T010 [P] Implement audio utility functions in `backend/src/utils/audio_utils.py` for format conversion (MP3/WAV to compatible format for Nemo) and chunking.
- [x] T011 [P] Implement basic structured logging middleware in `backend/src/middlewares/logging.py` using `python-json-logger`.
- [x] T012 [P] Implement Prometheus metrics middleware in `backend/src/middlewares/metrics.py` using `prometheus_client`.
- [x] T013 [P] Implement rate limiting middleware in `backend/src/middlewares/rate_limiter.py` using `fastapi-limiter` and Redis.
- [x] T014 [P] Load the `reazonspeech-nemo-v2` model once on app startup in `backend/src/core/stt_processor.py`. Include a method for transcribing audio data.

---

## Phase 3: User Story 1 - Transcribe Audio File (Priority: P1) 🎯 MVP

**Goal**: Implement the `/transcribe/file` endpoint for audio file transcription.
**Independent Test**: An API call with a Japanese audio file returns the correct text transcription, respecting authentication and rate limits.

### Tests for User Story 1 ⚠️
- [x] T015 [US1] Create integration test `backend/tests/test_file_transcribe.py` for the `/transcribe/file` endpoint to verify:
    - Successful transcription with valid audio and API key.
    - Error handling for invalid audio format.
    - Error handling for file size exceeding 50 MB.
    - Error handling for missing/invalid API key.
    - Error handling for rate limiting.

### Implementation for User Story 1
- [x] T016 [P] [US1] Implement the `/transcribe/file` POST endpoint in `backend/src/api/v1/endpoints/stt.py`.
- [x] T017 [US1] Integrate API Key authentication (`AuthDependency`) and rate limiting middleware to the `/transcribe/file` endpoint.
- [x] T018 [US1] Implement file upload handling, enforce 50 MB max size.
- [x] T019 [US1] Use `audio_utils.py` for audio format conversion and pass to `stt_processor.py` for transcription.
- [x] T020 [US1] Return `TranscriptionResult` in JSON format.
- [x] T021 [US1] Ensure structured logging and metrics are applied to this endpoint.

---

## Phase 4: User Story 2 - Transcribe Live Microphone Input (Priority: P2)

**Goal**: Implement the `/transcribe/stream` WebSocket endpoint for live audio transcription.
**Independent Test**: Streaming audio to the API results in continuous output of transcribed text with partial and final results and timestamps, respecting authentication and rate limits.

### Tests for User Story 2 ⚠️
- [x] T022 [US2] Create integration test `backend/tests/test_stream_transcribe.py` for the `/transcribe/stream` WebSocket endpoint to verify:
    - Successful continuous transcription with valid audio and API key.
    - Error handling for missing/invalid API key.
    - Error handling for rate limiting.
    - Correct output format (partial/final results with timestamps).

### Implementation for User Story 2
- [x] T023 [P] [US2] Implement the `/transcribe/stream` WebSocket endpoint in `backend/src/api/v1/endpoints/stt.py`.
- [x] T024 [US2] Integrate API Key authentication (`AuthDependency`) and rate limiting middleware to the `/transcribe/stream` endpoint.
- [x] T025 [US2] Handle incoming audio chunks from WebSocket, use `audio_utils.py` for processing/buffering.
- [x] T026 [US2] Integrate `stt_processor` for streaming transcription, sending back partial and final `TranscriptionResult` with timestamps.
- [x] T027 [US2] Ensure structured logging and metrics are applied to this endpoint.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Finalize operational aspects and documentation.

- [x] T028 Create `backend/Dockerfile` for deployment, including model download.
- [x] T029 Update root `README.md` to include instructions for setting up Redis and running the STT API.
- [x] T030 Ensure all requirements from `FR-010` (structured logging) and `FR-011` (Prometheus metrics) are fully implemented and integrated across all new endpoints.
- [x] T031 Verify the OpenAPI specification in `contracts/openapi.yaml` accurately reflects all implemented endpoints, security, and data models.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phase 2 (Foundational)** depends on Phase 1 completion.
- **Phase 3 (US1)** depends on Phase 2 completion.
- **Phase 4 (US2)** depends on Phase 2 completion.
- **Phase 5 (Polish)** depends on all previous phases.

## Parallel Execution Examples

### Parallel Tasks within Foundational Phase
- Tasks T008 through T014 can be worked on in parallel by different team members, as they are largely independent implementations of core services.

### Parallel User Story Implementation
- Once **Phase 2 (Foundational)** is complete, **Phase 3 (US1)** and **Phase 4 (US2)** can potentially be implemented in parallel if team capacity allows, as they represent distinct API endpoints. However, dependencies on `stt_processor` and middleware must be respected.
