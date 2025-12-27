# Research: Voice Interaction Orchestrator

This document summarizes the research and technical decisions for the STT -> LLM -> TTS orchestration.

## 1. FastAPI WebSocket Interleaving

- **Decision**: Use `websocket.receive()` and inspect the type or use `websocket.receive_text()` / `websocket.receive_bytes()` if the sequence is predictable. For interleaved data, a generic `receive()` loop is best.
- **Rationale**: The orchestrator must handle JSON control messages (e.g., `speech_start`, `config`) and raw PCM binary data asynchronously.
- **Alternatives considered**: Separate WebSockets for control and data. Rejected as it complicates synchronization and session management.

## 2. Low-Latency Pipeline (LLM -> TTS Streaming)

- **Decision**: Pipe LLM token stream into the TTS synthesizer. Synthesize audio as soon as a complete sentence or meaningful phrase is generated.
- **Rationale**: Generating the entire LLM response before starting TTS introduces unacceptable latency. Sentence-based synthesis balances latency and prosody quality.
- **Implementation Note**: Use `asyncio.Queue` to buffer tokens for the TTS stage.

## 3. User Barge-in (Task Cancellation)

- **Decision**: Wrap the LLM generation and TTS synthesis in an `asyncio.Task`. Upon receiving a `speech_start` event or significant audio energy from the client (VAD), trigger `task.cancel()`.
- **Rationale**: Immediate responsiveness is required to stop the AI from "talking over" the user.
- **Safety**: Ensure cancellation is handled gracefully using `try...except asyncio.CancelledError`.

## 4. Audio Format Synchronization

- **Decision**: Enforce 16kHz, 16-bit PCM (Mono) across the pipeline.
- **Rationale**: Standardized format avoids costly resampling between STT, LLM-orchestrator, and TTS stages.
- **Note**: The client is responsible for VAD and sending audio only when speech is present.
