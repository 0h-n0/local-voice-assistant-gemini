# Tasks: Project Scaffolding for Local Voice Assistant

**Input**: Design documents from `/specs/001-project-scaffolding/`
**Prerequisites**: plan.md, spec.md, contracts/, quickstart.md

**Tests**: Placeholder tests will be created to ensure the scaffolding is valid and test frameworks are configured correctly.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the basic directory structure for the entire project.

- [x] T001 Create the root project directories: `backend/`, `frontend/`, and `.github/workflows/`

---

## Phase 2: User Story 1 - Initialize Backend Project (Priority: P1) 🎯 MVP

**Goal**: Create a runnable FastAPI backend with basic security and configuration.
**Independent Test**: The backend server starts, and a GET request to `/health` returns a 200 OK response.

### Tests for User Story 1 ⚠️
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**
- [x] T002 [P] [US1] Create a test file `backend/tests/test_main.py` with a test that calls the `/health` endpoint and asserts a 200 status code.

### Implementation for User Story 1
- [x] T003 [P] [US1] Create a `backend/requirements.in` file with `fastapi`, `uvicorn[standard]`, and `pydantic`.
- [x] T004 [P] [US1] Create a `backend/.env.example` file to document environment variables for the backend.
- [x] T005 [US1] Create the main application file `backend/src/main.py` with a basic FastAPI app instance.
- [x] T006 [US1] Implement the `/health` endpoint in `backend/src/main.py` to return `{"status": "ok"}`.
- [x] T007 [US1] Configure basic CORS middleware in `backend/src/main.py` to allow requests from the frontend's development server address.
- [x] T008 [US1] Configure the backend to load environment variables from a `.env` file in `backend/src/main.py`.

---

## Phase 3: User Story 2 - Initialize Frontend Project (Priority: P1) 🎯 MVP

**Goal**: Create a runnable Next.js frontend that can be developed independently.
**Independent Test**: The Next.js development server starts and renders a placeholder page at the root URL.

### Tests for User Story 2 ⚠️
- [x] T009 [P] [US2] Create a basic Jest test file `frontend/tests/Home.test.tsx` that renders the main page component and asserts the main heading is present.

### Implementation for User Story 2
- [x] T010 [US2] Initialize a standard Next.js with TypeScript project in the `frontend/` directory using `npx create-next-app@latest`.
- [x] T011 [P] [US2] Create a `.env.local.example` file in `frontend/` to document environment variables.
- [x] T012 [US2] Modify the home page at `frontend/src/app/page.tsx` to display the title "Local Voice Assistant".
- [x] T013 [US2] Configure Jest for testing the Next.js application by creating `frontend/jest.config.js` and `frontend/jest.setup.js`.

---

## Phase 4: User Story 3 - Establish Project-Level Tooling (Priority: P2)

**Goal**: Configure project-wide linting and a CI workflow to ensure code quality.
**Independent Test**: The root `lint` command checks both projects, and the CI workflow runs successfully on a pull request.

### Implementation for User Story 3
- [x] T014 [P] [US3] Configure `ruff` for the backend by creating a `[tool.ruff]` section in `backend/pyproject.toml`.
- [x] T015 [P] [US3] Ensure `eslint` is configured for the frontend in `frontend/eslint.config.mjs` as part of the default Next.js setup.
- [x] T016 [US3] Create a root `package.json` file and add a `lint` script that concurrently runs `ruff check .` in `backend/` and `npm run lint` in `frontend/`.
- [x] T017 [US3] Create the CI workflow file at `.github/workflows/ci.yaml`.
- [x] T018 [US3] Implement the CI workflow in `.github/workflows/ci.yaml` to be triggered on pull requests, install all dependencies (backend and frontend), and run the root `lint` script.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Finalize documentation and validate the end-to-end developer experience.

- [x] T019 Create the main project `README.md` and populate it with the contents of `specs/001-project-scaffolding/quickstart.md`.
- [x] T020 Manually execute all steps in the `README.md` to ensure the developer setup is smooth and error-free.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phase 2 (US1)** and **Phase 3 (US2)** can be worked on in parallel after Phase 1 is complete.
- **Phase 4 (US3)** can be worked on in parallel with Phase 2 and 3, but its validation depends on their completion.
- **Phase 5 (Polish)** must be done last.
