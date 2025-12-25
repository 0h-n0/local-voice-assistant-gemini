# Quickstart: OpenAI LLM Service

This service provides an interface to OpenAI's `gpt-5-mini` model.

## Prerequisites
- Python 3.11+
- Valid OpenAI API Key

## Configuration
Set the following environment variable in a `.env` file in the `backend/` directory:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Running the Service
1. Navigate to the backend directory.
2. Install dependencies: `uv pip install -r requirements.in`.
3. Start the FastAPI server: `uvicorn src.main:app --reload`.

## Testing the API
Send a POST request to `/api/v1/llm/chat`:

### Batch Mode
```bash
curl -X POST http://localhost:8000/api/v1/llm/chat \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "Hello AI!"}],
  "stream": false
}'
```

### Streaming Mode
```bash
curl -X POST http://localhost:8000/api/v1/llm/chat \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "Tell me a long story."}],
  "stream": true
}'
```
