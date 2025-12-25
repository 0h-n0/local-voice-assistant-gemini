# Feature Specification: Project Scaffolding for Local Voice Assistant

**Feature Branch**: `001-project-scaffolding`  
**Created**: 2025-12-25
**Status**: Draft  
**Input**: User description: "ローカル音声アシスタントのバックエンドとフロントエンドの基本プロジェクト構成を作成したい。FastAPI + React (or Next.js) 構成。"

## Clarifications

### Session 2025-12-25
- Q: What level of baseline security should be configured in the initial FastAPI and Next.js projects? → A: Basic: Include .env file support for secrets and add default security headers (e.g., for CORS, XSS protection).
- Q: What initial Continuous Integration (CI) workflow should be included in the scaffolding? → A: PR Quality Check: A GitHub Actions workflow that runs linters for both frontend and backend on every push to a pull request.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Initialize Backend Project (Priority: P1)

As a developer, I want a standardized FastAPI project structure created so that I can immediately begin developing backend services for the voice assistant.

**Why this priority**: The backend is foundational for any frontend functionality.

**Independent Test**: The generated backend project can be started, and a health check endpoint returns a successful response.

**Acceptance Scenarios**:

1. **Given** a fresh clone of the repository, **When** I navigate to the `backend` directory and run the install command, **Then** all required dependencies specified in the constitution (`uv`, `pydantic`, `ruff`, `fastapi`) are installed.
2. **Given** the backend dependencies are installed, **When** I run the start command, **Then** the FastAPI server starts without errors.
3. **Given** the server is running, **When** I send a GET request to a `/health` endpoint, **Then** I receive a 200 OK response with a JSON body `{"status": "ok"}`.

---

### User Story 2 - Initialize Frontend Project (Priority: P1)

As a developer, I want a standardized Next.js with TypeScript project structure created so that I can rapidly build the user interface.

**Why this priority**: The frontend is essential for user interaction and is a parallel foundational component to the backend.

**Independent Test**: The generated frontend project can be started, and the default home page renders correctly in a browser.

**Acceptance Scenarios**:

1. **Given** a fresh clone of the repository, **When** I navigate to the `frontend` directory and run the install command, **Then** all required dependencies are installed.
2. **Given** the frontend dependencies are installed, **When** I run the start command, **Then** the Next.js development server starts without errors.
3. **Given** the server is running, **When** I open my browser to the specified local address, **Then** I see a placeholder page titled "Local Voice Assistant".

---

### User Story 3 - Establish Project-Level Tooling (Priority: P2)

As a developer, I want project-wide linting and formatting configured so that I can ensure code quality and consistency across both frontend and backend from the beginning.

**Why this priority**: Establishing quality gates early prevents technical debt.

**Independent Test**: Running a single lint command from the root of the project checks both frontend and backend codebases.

**Acceptance Scenarios**:

1. **Given** the repository is cloned, **When** I run a root-level lint command, **Then** `ruff` lints the backend code and `eslint` lints the frontend code.
2. **Given** I introduce a deliberate linting error in a backend Python file, **When** I run the lint command, **Then** the command exits with an error and reports the specific violation.
3. **Given** I introduce a deliberate linting error in a frontend TypeScript file, **When** I run the lint command, **Then** the command exits with an error and reports the specific violation.

---

### Edge Cases

- How does the setup handle different versions of Node.js or Python? (Assumption: The project's README will specify the required versions).
- What happens if a developer does not have `uv` or `npm`/`yarn` installed globally? (Assumption: The setup scripts will check for prerequisites).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a `backend` directory containing a FastAPI project structure.
- **FR-002**: The backend project MUST be pre-configured with `uv` for package management, `pydantic` for type validation, and `ruff` for linting, as per the constitution.
- **FR-003**: The backend project MUST include a placeholder `/health` endpoint.
- **FR-004**: The system MUST provide a `frontend` directory containing a Next.js (TypeScript) project.
- **FR-005**: The frontend project MUST be pre-configured with standard linting (`eslint`).
- **FR-006**: The frontend project MUST display a basic placeholder page.
- **FR-007**: The root of the repository MUST contain scripts to install dependencies and run linters for both projects simultaneously.
- **FR-008**: The backend project MUST be configured to use `.env` files for managing environment variables.
- **FR-009**: The backend project MUST include default middleware for common security headers (e.g., CORS).
- **FR-010**: The frontend project MUST be configured to use `.env` files for managing environment variables.
- **FR-011**: A GitHub Actions workflow file MUST be included in the `.github/workflows` directory.
- **FR-012**: The CI workflow MUST be triggered on every push to a pull request.
- **FR-013**: The CI workflow MUST execute the linting scripts for both the backend and frontend.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new developer can get both frontend and backend servers running locally within 5 minutes of cloning the repository, assuming all prerequisites are met.
- **SC-002**: 100% of pull requests MUST pass the CI linting checks before being eligible for merge.
- **SC-003**: The initial project scaffolding MUST receive a score of "A" on Code Climate or a similar static analysis tool.
- **SC-004**: The time to install all dependencies for a clean project clone MUST be under 2 minutes on a standard developer machine with a high-speed internet connection.