from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
import os
from fastapi import HTTPException
from fastapi_limiter import FastAPILimiter

# --- GLOBAL PATCHES (Applied BEFORE importing src.main or src.core.stt_processor) ---

# 1. Mock STTProcessor
mock_stt_instance = MagicMock()
async def mock_transcribe_stream_async_generator(*args, **kwargs):
    yield {"text": "ストリーミングモック", "is_final": False, "start_timestamp": 0.0, "end_timestamp": 0.5}
    yield {"text": "最終結果", "is_final": True, "start_timestamp": 0.5, "end_timestamp": 1.0}
mock_stt_instance.transcribe_stream.return_value = mock_transcribe_stream_async_generator()
mock_stt_instance.transcribe.return_value = "これはテストの文字起こしです"

# Patch the class and the instance at module level
patch('src.core.stt_processor.STTProcessor', return_value=mock_stt_instance).start()
patch('src.core.stt_processor.stt_processor', mock_stt_instance).start()

# 2. Mock FastAPILimiter and Redis
patch.object(FastAPILimiter, 'init', return_value=None).start()
patch('src.middlewares.rate_limiter.redis_client', MagicMock()).start()

# --- Now import app and dependencies ---
from src.main import app
from src.api.v1.dependencies import get_api_key
from src.middlewares.rate_limiter import rate_limit_dependency

client = TestClient(app)

# --- Tests ---

@pytest.fixture(autouse=True)
def setup_env_and_overrides(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_api_key")
    
    async def mock_rate_limiter_call():
        return None

    app.dependency_overrides[get_api_key] = lambda: "test_api_key"
    app.dependency_overrides[rate_limit_dependency] = mock_rate_limiter_call
    
    yield
    
    app.dependency_overrides.clear()

def test_successful_stream_transcription():
    with client.websocket_connect("/api/v1/transcribe/stream?api_key=test_api_key") as websocket:
        websocket.send_bytes(b"dummy_audio_chunk")
        data = websocket.receive_json()
        assert data["text"] == "ストリーミングモック"
        assert data["is_final"] is False
        
        data = websocket.receive_json()
        assert data["text"] == "最終結果"
        assert data["is_final"] is True

def test_missing_api_key_stream():
    app.dependency_overrides.clear()
    with pytest.raises(Exception):
        with client.websocket_connect("/api/v1/transcribe/stream") as websocket:
            pass

def test_invalid_api_key_stream():
    app.dependency_overrides.clear()
    with pytest.raises(Exception):
        with client.websocket_connect("/api/v1/transcribe/stream?api_key=wrong_key") as websocket:
            pass

def test_rate_limiting_stream():
    async def mock_rate_limiter_fail():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    app.dependency_overrides[rate_limit_dependency] = mock_rate_limiter_fail
    
    with pytest.raises(Exception):
        with client.websocket_connect("/api/v1/transcribe/stream?api_key=test_api_key") as websocket:
            pass