from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class OrchestratorConfig(BaseModel):
    stt_model: Optional[str] = Field(None, description="STT model to use")
    llm_model: Optional[str] = Field(None, description="LLM model to use")
    tts_voice: Optional[str] = Field(None, description="TTS voice to use")
    tts_style: Optional[str] = Field(None, description="TTS style to use")

class WebSocketEvent(BaseModel):
    type: str = Field(..., description="Event type: config, speech_start, transcript, error, processing_start")
    payload: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Event-specific data")
