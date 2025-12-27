# Data Model: Voice Interaction Orchestrator

This document defines the in-memory entities used for managing real-time voice sessions.

## Entities

### SessionContext
State maintained for the duration of a WebSocket connection.
- `session_id`: UUID - Unique identifier for the WebSocket session.
- `history`: List[ChatMessage] - Sequential history of user and assistant messages for context.
- `current_task`: Optional[asyncio.Task] - Reference to the currently running LLM/TTS task for cancellation.
- `config`: OrchestratorConfig - Active configuration for this session.

### ChatMessage
Represents a single turn in the conversation.
- `role`: String ("user", "assistant", "system")
- `content`: String - Text transcription or generated response.
- `timestamp`: DateTime

### OrchestratorConfig
Handshake configuration sent by the client.
- `stt_model`: String (optional)
- `llm_model`: String (optional)
- `tts_voice`: String (optional)
- `tts_style`: String (optional)

### WebSocketEvent
Structure for JSON control messages.
- `type`: String ("config", "speech_start", "transcript", "error", "processing_start")
- `payload`: Object - Event-specific data.
