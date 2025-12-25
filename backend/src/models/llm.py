"""LLM models."""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message model."""

    role: Literal["system", "user", "assistant"]
    content: str

class LLMRequest(BaseModel):
    """LLM request model."""

    messages: List[ChatMessage]
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    stream: bool = False

class LLMResponseUsage(BaseModel):
    """LLM response usage model."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class LLMResponse(BaseModel):
    """LLM response model."""

    content: str
    usage: LLMResponseUsage
    finish_reason: str
