from typing import List, Optional

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    text: str = Field(..., max_length=500, description="The Japanese text to synthesize.")
    model_id: Optional[str] = Field(None, description="The specific model/speaker to use.")
    style: Optional[str] = Field("Neutral", description="The emotion/style name.")
    style_weight: Optional[float] = Field(1.0, description="Intensity of the chosen style.")
    speed: Optional[float] = Field(1.0, ge=0.5, le=2.0, description="Speech rate.")
    pitch: Optional[float] = Field(1.0, description="Fundamental frequency scale.")
    stream: bool = Field(False, description="Whether to use chunked transfer encoding.")

class VoiceModel(BaseModel):
    id: str = Field(..., description="Unique identifier.")
    name: str = Field(..., description="Human-readable name.")
    styles: List[str] = Field(..., description="List of supported emotion style names.")
    sample_rate: int = Field(..., description="Default output sample rate.")

class AudioMetadata(BaseModel):
    format: str = "wav"
    sample_rate: int
    duration: Optional[float] = None
