import asyncio
from unittest.mock import MagicMock

import pytest

from src.core.orchestrator.processor import VoiceOrchestrator
from src.core.orchestrator.session import SessionContext


@pytest.mark.asyncio
async def test_voice_orchestrator_process_turn():
    # Mock services
    mock_stt = MagicMock()
    mock_stt.transcribe.return_value = "こんにちは"
    
    mock_llm = MagicMock()
    async def mock_stream_llm(*args, **kwargs):
        yield "こん"
        yield "にちは"
        yield "。"
    mock_llm.stream_chat_completion = mock_stream_llm
    
    mock_tts = MagicMock()
    async def mock_stream_tts(*args, **kwargs):
        yield b"audio_chunk_1"
        yield b"audio_chunk_2"
    mock_tts.synthesize_stream = mock_stream_tts
    
    orchestrator = VoiceOrchestrator(stt_service=mock_stt, llm_service=mock_llm, tts_service=mock_tts)
    session = SessionContext()
    
    audio_chunks = []
    async for chunk in orchestrator.process_audio_turn(b"input_audio", session):
        if isinstance(chunk, bytes):
            audio_chunks.append(chunk)
            
    assert len(audio_chunks) > 0
    assert b"audio_chunk_1" in audio_chunks
    
    # Check history
    assert len(session.history) == 2
    assert session.history[0].role == "user"
    assert session.history[0].content == "こんにちは"
    assert session.history[1].role == "assistant"
    assert session.history[1].content == "こんにちは。"

@pytest.mark.asyncio
async def test_voice_orchestrator_cancellation():
    mock_stt = MagicMock()
    mock_stt.transcribe.return_value = "こんにちは"
    
    mock_llm = MagicMock()
    async def mock_stream_llm(*args, **kwargs):
        await asyncio.sleep(5) # Simulate long generation
        yield "token"
    mock_llm.stream_chat_completion = mock_stream_llm
    
    mock_tts = MagicMock()
    
    orchestrator = VoiceOrchestrator(stt_service=mock_stt, llm_service=mock_llm, tts_service=mock_tts)
    session = SessionContext()
    
    task = asyncio.create_task(orchestrator.process_audio_turn(b"audio", session).__anext__())
    await asyncio.sleep(0.5) # Give it time to start
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        pass # Expected


