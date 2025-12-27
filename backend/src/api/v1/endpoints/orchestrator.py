import asyncio
import json
import logging

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from src.api.v1.tts_dependencies import get_synthesizer
from src.core.llm.service import llm_service
from src.core.orchestrator.processor import VoiceOrchestrator
from src.core.orchestrator.session import SessionContext
from src.core.stt_processor import stt_processor
from src.models.orchestrator import OrchestratorConfig, WebSocketEvent

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Orchestrator
# Note: In a production app, these should be managed via dependencies
orchestrator = VoiceOrchestrator(
    stt_service=stt_processor,
    llm_service=llm_service,
    tts_service=get_synthesizer()
)

@router.websocket("/ws")
async def orchestrator_ws(
    websocket: WebSocket,
    api_key: str = Query(..., alias="api_key")
):
    # Validate API Key manually for WebSocket
    # (Since WebSocket dependencies work differently)
    from src.api.v1.dependencies import API_KEY
    if api_key != API_KEY:
        await websocket.close(code=4003)
        return

    await websocket.accept()
    session = SessionContext()
    logger.info(f"New voice session started: {session.session_id}")

    try:
        while True:
            # Receive message (can be text/json or binary/audio)
            message = await websocket.receive()
            
            if "text" in message:
                # Handle JSON control messages
                data = json.loads(message["text"])
                event = WebSocketEvent(**data)
                
                if event.type == "config":
                    session.config = OrchestratorConfig(**event.payload)
                    logger.info(f"Session {session.session_id} config updated")
                
                elif event.type == "speech_start":
                    # Handle barge-in: cancel current processing
                    session.cancel_current_task()
                    logger.info(f"Barge-in detected for session {session.session_id}")

            elif "bytes" in message:
                # Handle raw audio data
                audio_bytes = message["bytes"]
                
                # Create a task for processing the turn to allow cancellation
                session.cancel_current_task()
                
                async def run_turn():
                    async for result in orchestrator.process_audio_turn(audio_bytes, session):
                        if isinstance(result, dict):
                            await websocket.send_json(result)
                        elif isinstance(result, bytes):
                            await websocket.send_bytes(result)

                session.current_task = asyncio.create_task(run_turn())

    except WebSocketDisconnect:
        logger.info(f"Voice session disconnected: {session.session_id}")
        session.cancel_current_task()
    except Exception as e:
        logger.error(f"Error in WebSocket session {session.session_id}: {e}", exc_info=True)
        await websocket.close(code=1011)
