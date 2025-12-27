# Tasks: Voice Interaction Orchestrator

**Input**: Design documents from `/specs/005-voice-orchestrator/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: TDD approach using `pytest` to validate streaming logic, session management, and barge-in handling.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description with file path`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Update `backend/requirements.in` with `websockets`
- [X] T002 [P] Create core directories: `backend/src/core/orchestrator`, `backend/tests/orchestrator`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and session management needed for all interaction modes

- [X] T003 Implement `SessionContext` and `ChatMessage` models in `backend/src/core/orchestrator/session.py`
- [X] T004 Implement `OrchestratorConfig` and `WebSocketEvent` Pydantic models in `backend/src/models/orchestrator.py`

---

## Phase 3: User Story 1 - Low-Latency Voice Interaction (Streaming) (Priority: P1) 🎯 MVP

**Goal**: Establish WebSocket streaming for real-time STT -> LLM -> TTS orchestration
**Independent Test**: Connect via WebSocket, stream audio, and receive synthesized audio chunks with TTFB < 3s

### Tests for US1 ⚠️
- [X] T005 [US1] Create unit test for stream processing in `backend/tests/orchestrator/test_processor.py`
- [X] T006 [US1] Create integration test for WebSocket interleaved frames in `backend/tests/orchestrator/test_integration.py`

### Implementation for US1
- [X] T007 [US1] Implement `VoiceOrchestrator` base class in `backend/src/core/orchestrator/processor.py` with STT integration
- [X] T008 [US1] Implement LLM-to-TTS sentence-based streaming logic in `backend/src/core/orchestrator/processor.py`
- [X] T009 [US1] Implement WebSocket endpoint at `/api/v1/orchestrator/ws` in `backend/src/api/v1/endpoints/orchestrator.py`
- [X] T010 [P] [US1] Register orchestrator router in `backend/src/main.py`

---

## Phase 4: User Story 2 - Multi-Turn Context & Barge-in (Priority: P2)

**Goal**: Support stateful conversations and user interruptions
**Independent Test**: Verify that the AI remembers previous turns and stops talking when user interrupts

### Tests for US2 ⚠️
- [X] T011 [US2] Create unit test for session history retention in `backend/tests/orchestrator/test_session.py`
- [X] T012 [US2] Add test cases for task cancellation during barge-in in `backend/tests/orchestrator/test_processor.py`

### Implementation for US2
- [X] T013 [US2] Update `VoiceOrchestrator` to include session history in LLM prompts in `backend/src/core/orchestrator/processor.py`
- [X] T014 [US2] Implement user "barge-in" task cancellation logic in `backend/src/api/v1/endpoints/orchestrator.py`

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Operational readiness, local testing, and documentation

- [X] T015 Integrate structured JSON logging for stage latencies in `backend/src/core/orchestrator/processor.py`
- [X] T016 Create orchestration CLI test utility in `backend/src/cli/orchestrate_test.py`
- [X] T017 Update root `README.md` with Orchestrator API documentation from `specs/005-voice-orchestrator/quickstart.md`
- [X] T018 Run final linting and type checking across all new files

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** must be completed first.
2. **Foundational (Phase 2)** depends on Phase 1.
3. **User Story 1 (Phase 3)** is the MVP and depends on Phase 2.
4. **User Story 2 (Phase 4)** depends on Phase 3.
5. **Polish (Final Phase)** depends on all previous phases.

## Parallel Execution Examples

- T002 (directories) and T001 (requirements) can run in parallel.
- T010 (router registration) can be done independently once the file exists.
- T016 (CLI tool) can be developed in parallel with integration testing.

## Implementation Strategy

- **MVP First**: Focus on Phase 3 to get a working single-turn streaming orchestrator.
- **Incremental**: Add session memory and barge-in in Phase 4 once the basic pipeline is stable.
