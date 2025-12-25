# Research: OpenAI LLM Service

This document summarizes the research and technical decisions for the OpenAI LLM Service.

## gpt-5-mini API Integration

- **Decision**: Use the `openai` Python SDK (v1.0+) `chat.completions.create` method.
- **Rationale**: Official SDK provides robust error handling, typing, and supports both synchronous and asynchronous calls.
- **Alternatives**: Using `httpx` directly. Rejected because the official SDK is better maintained and handles edge cases like exponential backoff.

## Streaming Implementation

- **Decision**: Use `stream=True` in OpenAI SDK and return a `StreamingResponse` from FastAPI using a generator.
- **Rationale**: Provides real-time token delivery to the frontend.
- **Alternatives**: WebSocket. Rejected because SSE (Server-Sent Events) is simpler for one-way streams and supported natively by the OpenAI SDK.

## Token Usage Tracking

- **Decision**: Log token counts (`prompt_tokens`, `completion_total`, `total_tokens`) from the `usage` field in the OpenAI response as part of a structured JSON log.
- **Rationale**: Meets the observability requirement without needing a database for the initial MVP.
- **Alternatives**: Database storage. Rejected for now to keep implementation simple (YAGNI).

## Error Mapping

- **Decision**: Map OpenAI error codes (e.g., `AuthenticationError`, `RateLimitError`) to internal `LLMServiceError` types with appropriate HTTP status codes.
- **Rationale**: Decouples the internal API from OpenAI-specific error structures.
