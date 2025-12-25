from typing import Optional

from pydantic import BaseModel


class AudioInput(BaseModel):
    type: str # "file" or "stream"
    data: bytes
    format: str # WAV, MP3, etc.

class TranscriptionResult(BaseModel):
    text: str
    confidence: Optional[float] = None
    is_final: bool
    start_timestamp: float
    end_timestamp: float
