import pytest
import respx
from httpx import Response

from src.core.llm.service import llm_service
from src.models.llm import ChatMessage, LLMRequest


@pytest.mark.asyncio
async def test_get_chat_completion_batch():
    # Mocking OpenAI API
    # OpenAI SDK v1.0+ uses httpx under the hood.
    # The endpoint is https://api.openai.com/v1/chat/completions

    with respx.mock:
        respx.post("https://api.openai.com/v1/chat/completions").mock(return_value=Response(
            200,
            json={
                "id": "chatcmpl-123",
                "object": "chat.completion",
                "created": 1677652288,
                "model": "gpt-5-mini",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Hello! How can I help you today?",
                    },
                    "finish_reason": "stop",
                }],
                "usage": {
                    "prompt_tokens": 9,
                    "completion_tokens": 12,
                    "total_tokens": 21
                }
            }
        ))

        request = LLMRequest(
            messages=[ChatMessage(role="user", content="Hi")],
            stream=False
        )

        response = await llm_service.get_chat_completion(request)

        assert response.content == "Hello! How can I help you today?"
        assert response.usage.total_tokens == 21
        assert response.finish_reason == "stop"

@pytest.mark.asyncio
async def test_get_chat_completion_stream():
    # Mocking OpenAI Streaming API
    with respx.mock:
        # SSE format: data: {...}\n\ndata: [DONE]\n\n
        stream_chunks = [
            'data: {"id":"1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant","content":"Hello"},"finish_reason":null}]}\n\n',
            'data: {"id":"1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":"stop"}]}\n\n',
            'data: [DONE]\n\n'
        ]
        
        async def stream_gen():
            for chunk in stream_chunks:
                yield chunk.encode("utf-8")
        
        respx.post("https://api.openai.com/v1/chat/completions").mock(return_value=Response(
            200,
            content=stream_gen(),
            headers={"Content-Type": "text/event-stream"}
        ))

        request = LLMRequest(
            messages=[ChatMessage(role="user", content="Hi")],
            stream=True
        )

        chunks = []
        async for chunk in llm_service.stream_chat_completion(request):
            chunks.append(chunk)

        assert len(chunks) == 2
        assert chunks[0] == "Hello"
        assert chunks[1] == "!"

@pytest.mark.asyncio
async def test_get_chat_completion_with_params():
    with respx.mock:
        # We want to check if the mocked request received the correct params
        route = respx.post("https://api.openai.com/v1/chat/completions").mock(return_value=Response(
            200,
            json={
                "choices": [{"message": {"content": "Deterministic response"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}
            }
        ))

        request = LLMRequest(
            messages=[ChatMessage(role="user", content="Hi")],
            temperature=0.0,
            max_tokens=10
        )

        await llm_service.get_chat_completion(request)

        # Check if the last request to respx had the correct body
        last_request = route.calls.last.request
        import json
        body = json.loads(last_request.content)
        assert body["temperature"] == 0.0
        assert body["max_tokens"] == 10

@pytest.mark.asyncio
async def test_openai_api_error_handling():
    with respx.mock:
        respx.post("https://api.openai.com/v1/chat/completions").mock(return_value=Response(
            401,
            json={"error": {"message": "Invalid API Key", "type": "invalid_request_error"}}
        ))

        request = LLMRequest(messages=[ChatMessage(role="user", content="Hi")])

        with pytest.raises(Exception) as excinfo:
            await llm_service.get_chat_completion(request)

        # In a real implementation we might have custom exception types
        # For now we check if it propagates or handles
        assert "401" in str(excinfo.value) or "Unauthorized" in str(excinfo.value)
