# Research: Japanese TTS API with Style-Bert-VITS2

This document summarizes the technical research and decisions for the TTS API implementation.

## 1. Style-Bert-VITS2 API Integration

- **Decision**: Use the official `style-bert-vits2` Python package.
- **Rationale**: Provides direct access to the inference engine, style vector manipulation, and Bert-based prosody processing.
- **Key Findings**:
    - Models are typically distributed as `.safetensors` or `.pth` files along with a `config.json` and style vectors.
    - Inference requires a specific Bert model (e.g., `JP-Extra`) for Japanese text processing.
    - Styles are mapped to specific IDs or names in the model configuration.

## 2. Audio Streaming (Chunked Transfer Encoding)

- **Decision**: Use FastAPI's `StreamingResponse` with a generator yielding binary chunks.
- **Rationale**: Allows the client to begin playback as soon as the first chunk of audio is received, significantly improving the user experience for longer texts.
- **Implementation Note**:
    - Must ensure proper WAV headers are sent or use a headerless (raw PCM) format if the client supports it (spec says WAV MUST be returned, so we will use a streaming-compatible WAV wrapper or small chunks with a valid first chunk).
    - For real-time streaming, we will generate audio in segments (e.g., by sentence) and stream them sequentially.

## 3. Concurrency and Resource Management

- **Decision**: Implement a simple semaphore-based lock to limit concurrent heavy inference tasks to 2 (as per SC-003).
- **Rationale**: TTS inference is CPU/GPU intensive. Overloading the server leads to extreme latency spikes for all users.
- **Alternatives**: Using a task queue (e.g., Celery). Rejected for MVP as it adds unnecessary complexity (YAGNI).

## 4. API Key and Rate Limiting

- **Decision**: Standardize on the `APIKeyHeader` pattern used in the STT/LLM services.
- **Rationale**: Consistency across the backend services simplifies developer integration.
