from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect, status

from src.api.v1.dependencies import get_api_key
from src.core.stt_processor import stt_processor
from src.middlewares.rate_limiter import rate_limit_dependency  # Import shared rate limit dependency
from src.models.stt_models import TranscriptionResult
from src.utils.audio_utils import convert_audio_to_wav, get_audio_duration  # Import convert_audio_to_wav

router = APIRouter()

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

@router.post(
    "/transcribe/file",
    response_model=TranscriptionResult,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limit_dependency)] # Use shared rate limit dependency
)
async def transcribe_file(
    api_key: Annotated[str, Depends(get_api_key)],
    audio_file: UploadFile = File(...),
):
    # Validate file type
    if audio_file.content_type not in ["audio/wav", "audio/mpeg"]: # audio/mpeg for MP3
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported media type: {audio_file.content_type}. Only WAV and MP3 are supported.",
        )

    # Validate file size
    file_contents = await audio_file.read()
    if len(file_contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds {MAX_FILE_SIZE_MB}MB limit.",
        )

    # Convert audio to WAV format compatible with Nemo
    try:
        wav_audio_bytes = convert_audio_to_wav(file_contents, audio_file.content_type.split('/')[-1])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Audio conversion failed: {e}")

    try:
        transcribed_text = stt_processor.transcribe(wav_audio_bytes)

        # Dummy timestamps and confidence for now
        duration = get_audio_duration(file_contents, audio_file.content_type.split('/')[-1])

        return TranscriptionResult(
            text=transcribed_text,
            confidence=None,
            is_final=True,
            start_timestamp=0.0,
            end_timestamp=duration,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.websocket("/transcribe/stream")
async def transcribe_stream(
    websocket: WebSocket,
    api_key: str = Depends(get_api_key),
    rate_limit: None = Depends(rate_limit_dependency) # Use shared rate limit dependency
):
    await websocket.accept()
    try:
        async def audio_generator():
            while True:
                data = await websocket.receive_bytes()
                yield data

        async for result in stt_processor.transcribe_stream(audio_generator()):
            await websocket.send_json(result)
            if result.get("is_final"):
                break
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
