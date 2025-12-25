"""LLM service logic."""

import json

import openai
from fastapi import HTTPException

from src.core.llm.client import openai_client
from src.models.llm import LLMRequest, LLMResponse, LLMResponseUsage
from src.utils.logging import log_llm_usage


class LLMService:
    """Service for handling LLM requests."""

    async def get_chat_completion(self, request: LLMRequest) -> LLMResponse:
        """Get a non-streaming chat completion."""
        try:
            messages = [m.model_dump() for m in request.messages]
            response = await openai_client.create_chat_completion(
                messages=messages, temperature=request.temperature, max_tokens=request.max_tokens, stream=False
            )

            content = response.choices[0].message.content
            usage_data = response.usage
            finish_reason = response.choices[0].finish_reason

            usage = LLMResponseUsage(
                prompt_tokens=usage_data.prompt_tokens,
                completion_tokens=usage_data.completion_tokens,
                total_tokens=usage_data.total_tokens,
            )

            log_llm_usage(
                model=openai_client.model,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
            )

            return LLMResponse(content=content, usage=usage, finish_reason=finish_reason)
        except openai.AuthenticationError:
            raise HTTPException(status_code=401, detail="OpenAI Authentication failed")
        except openai.RateLimitError:
            raise HTTPException(status_code=429, detail="OpenAI Rate limit exceeded")
        except openai.APIError as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Service internal error: {str(e)}")

    async def stream_chat_completion(self, request: LLMRequest):
        """Stream chat completion tokens."""
        try:
            messages = [m.model_dump() for m in request.messages]
            stream = await openai_client.create_chat_completion(
                messages=messages, temperature=request.temperature, max_tokens=request.max_tokens, stream=True
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

                if hasattr(chunk, "usage") and chunk.usage:
                    log_llm_usage(
                        model=openai_client.model,
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                    )
        except openai.AuthenticationError:
            yield json.dumps({"error": "Authentication failed"})
        except openai.RateLimitError:
            yield json.dumps({"error": "Rate limit exceeded"})
        except Exception as e:
            yield json.dumps({"error": str(e)})


llm_service = LLMService()
