# Data Model: OpenAI LLM Service

This document defines the data structures used by the LLM service.

## Entities

### ChatMessage
Represents a single message in a conversation.
- `role`: String (one of: `system`, `user`, `assistant`)
- `content`: String (the text content of the message)

### LLMRequest
Input payload for the chat completion endpoint.
- `messages`: List[`ChatMessage`] (history of the conversation)
- `temperature`: Float (optional, default: 1.0)
- `max_tokens`: Integer (optional)
- `stream`: Boolean (optional, default: false)

### LLMResponse
Output payload for non-streaming chat completion.
- `content`: String (the generated response text)
- `usage`: Object
    - `prompt_tokens`: Integer
    - `completion_tokens`: Integer
    - `total_tokens`: Integer
- `finish_reason`: String

## State Transitions
N/A (Stateless API)
