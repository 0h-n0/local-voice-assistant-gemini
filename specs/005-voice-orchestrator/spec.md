# Feature Specification: Voice Interaction Orchestrator

**Feature Branch**: `005-voice-orchestrator`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "STT → LLM → TTSを順番に実行し、1つの音声対話を完結させるオーケストレーターを実装したい"

## Clarifications

### Session 2025-12-27
- Q: Which part of the system should handle Voice Activity Detection (VAD)? → A: Client-side VAD (Client sends audio only when speech is detected).
- Q: How should JSON control messages and Binary audio data be handled on the WebSocket? → A: JSON + Binary Interleaving (Text frames for JSON, Binary frames for audio).
- Q: How should the system handle user "barge-in" (user speaks while AI is responding)? → A: Stop and Reset (Cancel current AI generation immediately).
- Q: How should conversation history be persisted? → A: In-memory (Session-bound, history cleared on disconnect).
- Q: What is the preferred audio format for the WebSocket stream? → A: 16kHz, 16-bit PCM (Mono).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Low-Latency Voice Interaction (Streaming) (Priority: P1)

A user connects via WebSocket and speaks a query. The system streams back the audio response in near real-time, creating a fluid conversational experience.

**Why this priority**: Low latency is critical for voice interfaces. Waiting for full processing breaks the illusion of conversation.

**Independent Test**: Connect a WebSocket client, stream a WAV chunk containing "こんにちは", and verify that the server begins streaming back audio chunks within 3 seconds.

**Acceptance Scenarios**:

1. **Given** a WebSocket connection is established, **When** the user sends audio data, **Then** the system returns synthesized audio chunks as they are generated (Time to First Byte < 3s).
2. **Given** an ongoing response, **When** the client disconnects, **Then** the server aborts processing to save resources.

---

### User Story 2 - Multi-Turn Context (Priority: P2)

A user asks a follow-up question (e.g., "Sore wa nani?") without restating the subject. The system understands the context from the previous turn and answers correctly.

**Why this priority**: Enables natural conversation beyond simple one-off commands.

**Independent Test**:
1. Send "Who is the Prime Minister of Japan?" -> Verify answer.
2. Send "How old is he?" -> Verify answer refers to the PM mentioned in step 1.

**Acceptance Scenarios**:

1. **Given** a user has just asked "Who is Natsume Soseki?", **When** the user asks "What did he write?", **Then** the system responds with Soseki's works (e.g., "Kokoro", "Botchan").
2. **Given** a WebSocket session is closed, **When** a new session starts, **Then** the conversation history is reset (clean slate).

### Edge Cases

- **Service Failure**: If STT or LLM fails mid-stream, the system sends a specific JSON error message over the WebSocket before closing.
- **Unsynthesizable Text**: If LLM generates text that TTS cannot handle (e.g., ASCII art), it is filtered out before synthesis.
- **Timeout**: If no audio is detected for a specific duration (e.g., 30s), the server closes the connection with a timeout code.
- **User Barge-in**: If the client sends a `speech_start` event or new audio while the server is currently sending response audio, the server MUST stop generation and transmission for the current turn immediately.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a WebSocket endpoint at `/api/v1/orchestrator/ws` supporting interleaved Text (JSON) and Binary (Audio) frames.
- **FR-002**: System MUST accept binary audio chunks from the client in **16kHz, 16-bit PCM (Mono)** format, assuming client-side Voice Activity Detection (VAD).
- **FR-003**: System MUST convert input audio to text using the internal STT service.
- **FR-004**: System MUST generate a response using the internal LLM service, maintaining conversation context for the duration of the WebSocket session.
- **FR-005**: System MUST convert the LLM text response to audio using the internal TTS service.
- **FR-006**: System MUST stream output audio chunks in **16kHz, 16-bit PCM (Mono)** to the client immediately upon generation to minimize latency.
- **FR-007**: System MUST maintain conversation context in-memory for the duration of the WebSocket session and clear it upon disconnection.

### Key Entities

- **SessionContext**: In-memory store for the list of `ChatMessage` (user/assistant) for the current WebSocket connection.
- **OrchestratorConfig**: Configuration for sub-services (model selection, voice style) passed during connection handshake.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Time to First Audio Byte (TTFB) is **< 3 seconds** for a standard short query.
- **SC-002**: System successfully handles multi-turn context for at least 3 consecutive turns in 90% of test sessions.
- **SC-003**: System gracefully handles service interruptions by sending a structured error frame within 1 second of failure detection.
