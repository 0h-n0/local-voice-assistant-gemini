# Tasks: Japanese TTS API with Style-Bert-VITS2

**Input**: Design documents from `/specs/004-tts-japanese-api/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/openapi.yaml

**Tests**: TDD approach using `pytest` to validate audio output and parameter application.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description with file path`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Update `backend/requirements.in` with `style-bert-vits2` and `pydub`
- [X] T002 [P] Create core directories: `backend/src/core/tts`, `backend/src/api/v1/endpoints`, `backend/src/models`, `backend/tests/tts`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and synthesis logic needed for all endpoints

- [X] T003 Create TTS Pydantic models in `backend/src/models/tts.py` (`TTSRequest`, `VoiceModel`)
- [X] T004 Implement `ModelManager` in `backend/src/core/tts/model_manager.py` to handle Style-Bert-VITS2 model loading and style mapping
- [X] T005 Implement `Synthesizer` in `backend/src/core/tts/synthesizer.py` for text-to-audio inference
- [X] T006 [P] Implement audio utilities in `backend/src/utils/audio.py` for WAV header construction and chunking

---

## Phase 3: User Story 1 & 2 - Core Synthesis (Batch & Stream) (Priority: P1) 🎯 MVP

**Goal**: Support high-quality Japanese voice synthesis in both batch and real-time streaming modes
**Independent Test**: Call `/synthesize` and receive valid audio data (full WAV and SSE/chunked)

### Tests for Core Synthesis ⚠️
- [X] T007 [US1] Create integration test `backend/tests/tts/test_api.py` for batch synthesis (WAV integrity check)
- [X] T008 [US2] Add streaming test cases to `backend/tests/tts/test_api.py` to verify chunked transfer encoding

### Implementation for Core Synthesis
- [X] T009 [US1] Implement `/synthesize` POST endpoint in `backend/src/api/v1/endpoints/tts.py` (batch mode)
- [X] T010 [US2] Implement `/synthesize` streaming logic using FastAPI `StreamingResponse`
- [X] T011 [US1, US2] Implement semaphore-based concurrency control in `backend/src/core/tts/synthesizer.py` (limit to 2 concurrent sessions)
- [X] T012 [P] Register TTS router in `backend/src/main.py`

---

## Phase 4: User Story 3 - Style Control & Parameters (Priority: P2)

**Goal**: Allow fine-tuning of emotions and voice characteristics
**Independent Test**: Verify that style and speed parameters result in audible prosody changes

### Tests for Style & Parameters ⚠️
- [X] T013 [US3] Add tests for `style`, `speed`, and `pitch` parameter application in `backend/tests/tts/test_synthesis.py`

### Implementation for Style & Parameters
- [X] T014 [US3] Update `Synthesizer` to support `style_weight`, `speed`, and `pitch`
- [X] T015 [P] Implement `/models` GET endpoint in `backend/src/api/v1/endpoints/tts.py` to list available speakers and styles

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Operational readiness and documentation

- [X] T016 Integrate structured JSON logging for synthesis requests (character count, inference duration) in `backend/src/core/tts/service.py`
- [X] T017 [P] Implement Prometheus metrics for TTS service (synthesized characters total, inference time histogram)
- [X] T018 Create testing CLI in `backend/src/cli/tts_cli.py`
- [X] T019 Update root `README.md` with TTS API documentation from `specs/004-tts-japanese-api/quickstart.md`
- [X] T020 Run final linting and type checking across all new files

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** must be completed first.
2. **Foundational (Phase 2)** depends on Phase 1.
3. **Core Synthesis (Phase 3)** depends on Phase 2.
4. **Style & Parameters (Phase 4)** depends on Phase 3.
5. **Polish (Final Phase)** depends on all previous phases.

## Parallel Execution Examples

- T002 and T006 can run in parallel with directory setup.
- T012 (router registration) can be done independently once the file exists.
- T017 (metrics) can be developed in parallel with service logic.

## Implementation Strategy

- **MVP First**: Focus on Phases 1, 2, and 3 to get a working synthesis API.
- **Incremental**: Add style control and model listing in Phase 4.
