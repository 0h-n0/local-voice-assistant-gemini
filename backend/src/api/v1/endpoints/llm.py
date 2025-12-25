"""LLM API endpoints."""

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.core.llm.service import llm_service
from src.models.llm import LLMRequest, LLMResponse

router = APIRouter()


@router.post("/chat", response_model=LLMResponse)
async def chat_completion(request: LLMRequest):
    """Generate a chat completion response from the LLM."""
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty")

    if request.stream:

        async def event_generator():
            async for chunk in llm_service.stream_chat_completion(request):
                # SSE format: data: <json>\n\n
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    return await llm_service.get_chat_completion(request)
