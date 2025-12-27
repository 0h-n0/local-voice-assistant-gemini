import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse

from backend.src.api.v1.dependencies import get_api_key
from backend.src.api.v1.tts_dependencies import get_synthesizer, get_model_manager
from backend.src.core.tts.model_manager import ModelManager
from backend.src.core.tts.synthesizer import Synthesizer
from backend.src.models.tts import TTSRequest, VoiceModel

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/synthesize", dependencies=[Depends(get_api_key)])
async def synthesize(
    request: TTSRequest,
    synthesizer: Synthesizer = Depends(get_synthesizer)
):
    """
    Synthesize Japanese text to speech.
    Supports both batch (wait for full audio) and streaming modes.
    """
    try:
        if request.stream:
            return StreamingResponse(
                synthesizer.synthesize_stream(request),
                media_type="audio/wav"
            )
        else:
            audio_data = await synthesizer.synthesize(request)
            return Response(content=audio_data, media_type="audio/wav")
    except ValueError as e:
        logger.warning(f"TTS Bad Request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"TTS Synthesis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal synthesis error")

@router.get("/models", response_model=List[VoiceModel], dependencies=[Depends(get_api_key)])
async def list_models(
    model_manager: ModelManager = Depends(get_model_manager)
):
    """List available voice models and their styles."""
    return model_manager.list_models()