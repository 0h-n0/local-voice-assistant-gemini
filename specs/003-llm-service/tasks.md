# Tasks: OpenAI LLM Service

**Input**: Design documents from `/specs/003-llm-service/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/openapi.yaml

**Tests**: TDD approach using `pytest` and `respx` for API simulation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description with file path`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Update `backend/requirements.in` with `openai` and `respx`
- [x] T002 [P] Create directories: `backend/src/core/llm`, `backend/src/models`, `backend/src/api/v1/endpoints`, `backend/tests/integration`
- [x] T003 Add `OPENAI_API_KEY` to `backend/.env.example`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and utilities needed for all user stories

- [x] T004 Create LLM Pydantic models in `backend/src/models/llm.py` (`ChatMessage`, `LLMRequest`, `LLMResponse`)
- [x] T005 [P] Implement structured JSON logging utility in `backend/src/utils/logging.py`
- [x] T006 Implement base OpenAI client wrapper in `backend/src/core/llm/client.py`

---

## Phase 3: User Story 1 & 2 - Chat Completion (Batch & Stream) (Priority: P1) 🎯 MVP

**Goal**: Support multi-turn chat conversations with both batch and streaming response modes
**Independent Test**: Send chat history and verify gpt-5-mini response (batch and stream)

### Tests for Chat Completion ⚠️
- [x] T007 [US1] Create integration test `backend/tests/integration/test_llm.py` for batch chat completion using `respx`
- [x] T008 [US2] Add streaming (SSE) test cases to `backend/tests/integration/test_llm.py`

### Implementation for Chat Completion
- [x] T009 [US1] Implement `LLMService.get_chat_completion` in `backend/src/core/llm/service.py` (batch mode)
- [x] T010 [US2] Implement `LLMService.stream_chat_completion` in `backend/src/core/llm/service.py` (generator for SSE)
- [x] T011 [US1, US2] Create API endpoint in `backend/src/api/v1/endpoints/llm.py`
- [x] T012 [US1, US2] Integrate token usage tracking and structured logging in `LLMService`
- [x] T013 [P] Register llm router in `backend/src/main.py`

---

## Phase 4: User Story 3 & 4 - Parameters & Error Handling (Priority: P2)

**Goal**: Support creative parameters and handle API failures gracefully
**Independent Test**: Verify temperature impacts and verify error mapping (e.g., 401 -> Internal Auth Error)

### Tests for Parameters & Errors ⚠️
- [x] T014 [US3] Add tests for parameter passing (temperature, max_tokens) in `backend/tests/integration/test_llm.py`
- [x] T015 [US4] Add error mapping tests (401, 429, 500) in `backend/tests/integration/test_llm.py`

### Implementation for Parameters & Errors
- [x] T016 [US3] Update `OpenAIClient` and `LLMService` to support optional parameters
- [x] T017 [US4] Implement `LLMServiceError` and mapping logic in `backend/src/core/llm/service.py`

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Testing tools and final validation

- [x] T018 Create testing CLI in `backend/src/cli/llm_test.py`
- [x] T019 Update root `README.md` with LLM service details from `specs/003-llm-service/quickstart.md`
- [x] T020 Run final linting and type checking across all new files

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** must be completed first.
2. **Foundational (Phase 2)** depends on Phase 1.
3. **Chat Completion (Phase 3)** depends on Phase 2.
4. **Parameters & Error Handling (Phase 4)** depends on Phase 3.
5. **Polish (Final Phase)** depends on all previous phases.

## Parallel Execution Examples

- T002 and T003 can run in parallel.
- T004 and T005 can run in parallel.
- T013 can be done while service logic is being implemented.

## Implementation Strategy

- **MVP First**: Focus on Phase 1, 2, and 3 to get a working chat API.
- **Incremental**: Add parameter support and advanced error handling in Phase 4.
