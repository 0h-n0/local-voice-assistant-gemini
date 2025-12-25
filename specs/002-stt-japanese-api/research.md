# Research: Japanese STT API Integration Decisions

This document details the decisions and rationale for integrating the `reazon-research/reazonspeech-nemo-v2` model and related non-functional requirements into the FastAPI application.

## 1. STT Model Integration (`reazon-research/reazonspeech-nemo-v2`)

- **Decision**: The `reazonspeech-nemo-v2` model will be integrated using `nemo_toolkit[asr]`. The model will be loaded once on application startup into memory to minimize latency for subsequent requests. Inference will be performed asynchronously.
- **Rationale**: `nemo_toolkit` provides direct access to the model, ensuring optimal performance and full control over the STT process. Loading the model once avoids repetitive disk I/O and setup overhead. Asynchronous inference ensures the FastAPI application remains responsive during long-running transcription tasks.
- **Alternatives considered**:
    - Running the model in a separate microservice: This adds significant complexity (inter-service communication, deployment overhead) for this initial phase without clear benefits given the expected scale.
    - Using a cloud-based STT service: Does not meet the "local voice assistant" requirement and potentially increases cost and latency.

## 2. Audio Processing (WAV/MP3 decoding, resampling, chunking)

- **Decision**: For audio file uploads, `soundfile` will be used for reading and `pydub` for format conversion (e.g., MP3 to WAV) and resampling if necessary, to ensure compatibility with `nemo_toolkit`. For streaming, audio chunks received via WebSocket will be buffered and processed, potentially using `soundfile` or `pydub` for in-memory processing.
- **Rationale**: `soundfile` offers robust and efficient reading/writing of various audio formats. `pydub` simplifies audio manipulation tasks like conversion and resampling. Ensuring consistent audio format (e.g., 16kHz, mono, 16-bit PCM WAV) is crucial for optimal `nemo_toolkit` performance.
- **Alternatives considered**:
    - `librosa`: While powerful for audio analysis, it's more heavy-duty than needed for basic format conversion and often brings significant dependencies.
    - Custom audio processing: Too complex and error-prone; leveraging existing, well-tested libraries is preferred.

## 3. API Key Authentication

- **Decision**: Implement API Key authentication using FastAPI's `Security` dependency with `APIKeyHeader` or `APIKeyQuery`. Keys will be stored as environment variables.
- **Rationale**: FastAPI's built-in `Security` utilities provide a streamlined way to enforce authentication on endpoints. API Keys offer a simple and effective security mechanism for internal or controlled access to the API, meeting the FR-009 requirement.
- **Alternatives considered**:
    - Custom middleware: More boilerplate code than necessary.
    - OAuth2/JWT: Overkill for the current requirements but can be easily integrated later if more complex user management is needed.

## 4. Rate Limiting

- **Decision**: Implement basic rate limiting using `fastapi-limiter` integrated with Redis. Limits will be applied per API Key or IP address as specified (FR-012).
- **Rationale**: `fastapi-limiter` is a well-regarded library for FastAPI that provides robust and flexible rate-limiting capabilities. Using Redis as a backend ensures efficient and scalable rate limiting across multiple API instances if needed.
- **Alternatives considered**:
    - Custom rate-limiting middleware: Requires significant development and testing effort.
    - Cloud provider's API Gateway rate limiting: While effective, it ties the solution to a specific cloud provider and might be an additional cost.

## 5. Observability (Structured Logging & Prometheus Metrics)

- **Decision**:
    - **Structured Logging**: Implement structured logging using Python's standard `logging` module configured with a JSON formatter (e.g., `python-json-logger`). Log key request/response details as per FR-010.
    - **Prometheus Metrics**: Use `prometheus_client` to expose metrics like request count (`fastapi_requests_total`), request duration (`fastapi_request_duration_seconds`), and error rates (`fastapi_request_errors_total`) for each endpoint.
- **Rationale**: Structured logs are easily parseable by log aggregation systems, improving debuggability and monitoring. Prometheus metrics provide real-time visibility into API health and performance, aligning with FR-011 and enabling proactive issue detection.
- **Alternatives considered**:
    - `structlog`: A more advanced structured logging library. While powerful, `python-json-logger` is sufficient for basic requirements and simpler to integrate with the standard `logging` module.
    - Custom metric collection: More error-prone and less standardized than `prometheus_client`.

## 6. WebSocket Library for Streaming

- **Decision**: Utilize FastAPI's native WebSocket support, which leverages `websockets` under the hood. Audio chunks will be received and processed by `nemo_toolkit`'s streaming capabilities.
- **Rationale**: FastAPI's WebSocket capabilities are robust and well-integrated. It simplifies handling WebSocket connections and message passing. The `nemo_toolkit` is designed to handle audio streams, making this a natural fit.
- **Alternatives considered**:
    - Raw `websockets` library: FastAPI's abstraction simplifies development.
    - Third-party streaming libraries: Not necessary given FastAPI's native support.
