# Feature Specification: OpenAI LLM Service

**Feature Branch**: `003-llm-service`  
**Created**: 2025-12-25  
**Status**: Draft  
**Input**: User description: "OpenAI の gpt-5-mini に問い合わせてテキスト応答を生成する LLM サービスを実装したい。"

## Clarifications

### Session 2025-12-25
- Q: Should the service support streaming the AI's response token-by-token, or is a standard batch response sufficient? → A: Both. The system must support both batch and streaming (Server-Sent Events) responses, selectable by the caller.
- Q: Does the service need to support multi-turn conversations (maintaining a history of messages), or is it limited to single-turn prompt/response completions? → A: Chat History Support: The interface accepts a list of messages (history) with roles (user, assistant, system).
- Q: How should the OpenAI API Key and other service-level configurations be managed? → A: Environment Variables: Load secrets from a .env file or system environment variables.
- Q: How should token usage and request logs be handled? → A: Structured Logging: Log request metadata and token usage as structured JSON for later analysis.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-turn Chat Completion (Priority: P1)

As a user of the assistant, I want to have a continuous conversation where the AI remembers previous context so that I don't have to repeat information.

**Why this priority**: Core functionality for a natural conversational assistant.

**Independent Test**: Send a sequence of two prompts ("My name is Gemini", then "What is my name?") and verify the second response correctly identifies the user.

**Acceptance Scenarios**:

1. **Given** a sequence of valid chat messages, **When** the LLM service is queried in batch mode, **Then** it returns a non-empty text response from `gpt-5-mini` considering the history.
2. **Given** a conversation history that exceeds the model's token limit, **When** queried, **Then** the service returns a clear error message or handles context truncation.

---

### User Story 2 - Streaming Response (Priority: P1)

As a user, I want to see the AI's response appear in real-time as it is generated so that the interaction feels immediate and snappy.

**Why this priority**: Significant improvement to perceived performance and user experience.

**Independent Test**: Initiate a streaming request and verify that multiple data chunks are received via SSE before the connection closes.

**Acceptance Scenarios**:

1. **Given** a valid user prompt, **When** the service is queried in streaming mode, **Then** it sends a stream of tokens as Server-Sent Events (SSE).
2. **Given** a streaming connection, **When** the generation is finished, **Then** the stream terminates with a final termination signal or close.

---

### User Story 3 - Parameter Configuration (Priority: P2)

As a developer, I want to configure model parameters like temperature and max tokens so that I can control the creativity and length of the AI's response.

**Why this priority**: Essential for fine-tuning the assistant's behavior.

**Independent Test**: Query the service with `temperature=0` and verify that the output is highly deterministic across multiple identical queries.

**Acceptance Scenarios**:

1. **Given** specific parameters (temperature, max_tokens), **When** the service is called, **Then** the underlying API call to OpenAI includes these parameters.

---

### User Story 4 - Robust Error Handling (Priority: P2)

As a system, I want to handle OpenAI API failures gracefully (timeouts, rate limits, invalid keys) so that the user receives a helpful error message instead of a crash.

**Why this priority**: Reliability and user experience.

**Independent Test**: Temporarily use an invalid API key and verify that the system returns an "Unauthorized" or "Configuration error" message.

**Acceptance Scenarios**:

1. **Given** an expired or invalid OpenAI API key, **When** queried, **Then** the system returns a specific authentication error.
2. **Given** OpenAI API is rate-limited, **When** queried, **Then** the system implements a retry mechanism or returns a "Service busy" message.

---

### Edge Cases

- How does the system handle an empty prompt? (Assumption: It should reject it with a validation error).
- What happens if the network connection is lost during the request? (Assumption: It should timeout and return a network error).
- Handling non-textual responses or unexpected JSON structures from the API.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an interface to send a sequence of chat messages (history) to the OpenAI `gpt-5-mini` model.
- **FR-002**: System MUST retrieve and return the text content of the AI's response.
- **FR-003**: System MUST support optional configuration for `temperature` (0.0 to 2.0).
- **FR-004**: System MUST support optional configuration for `max_tokens`.
- **FR-005**: System MUST validate that the message list is not empty and each message has valid content.
- **FR-006**: System MUST handle OpenAI API errors (401, 429, 500) and map them to internal error types.
- **FR-007**: System MUST support both batch and streaming (Server-Sent Events) responses, selectable by the caller.
- **FR-008**: System MUST load the OpenAI API key and other service-level configurations from environment variables (e.g., using a `.env` file).

### Key Entities *(include if feature involves data)*

- **ChatMessage**: Contains a `role` (system, user, assistant) and string `content`.
- **LLMRequest**: Contains a list of **ChatMessage** objects (history), mode (batch/stream), and configuration parameters (temperature, model, etc.).
- **LLMResponse**: Contains the generated text, usage statistics (tokens), and finish reason.
- **LLMStreamChunk**: An individual data packet sent via SSE containing a fragment of text.
- **ServiceConfig**: Internal storage for API keys and endpoint URLs, initialized from environment variables.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of non-streaming requests return a response in under 3 seconds (excluding model processing time).
- **SC-002**: Zero hard crashes occur during API downtime; all errors are caught and logged.
- **SC-003**: Successfully integrates with the OpenAI `gpt-5-mini` endpoint as per their API documentation.
- **SC-004**: Usage of tokens and request metadata is accurately tracked and logged as structured JSON for every request.
