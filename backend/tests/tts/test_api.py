import os
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

# Ensure API Key is set for testing
os.environ["API_KEY"] = "test_secret"

from backend.src.api.v1.tts_dependencies import get_synthesizer
from backend.src.main import app

client = TestClient(app)

@pytest.fixture
def mock_synthesizer():
    # Use dependency override instead of patching global variable
    mock = MagicMock()
    
    # Default behavior for batch
    mock.synthesize = AsyncMock(return_value=b"fake_wav_header_and_data")
    
    app.dependency_overrides[get_synthesizer] = lambda: mock
    yield mock
    app.dependency_overrides = {}

def test_synthesize_batch_success(mock_synthesizer):
    # Setup specific mock behavior if needed (already set in fixture)
    
    payload = {
        "text": "こんにちは",
        "stream": False,
        "style": "Happy"
    }
    
    response = client.post(
        "/api/v1/tts/synthesize",
        json=payload,
        headers={"X-API-Key": "test_secret"}
    )
    
    assert response.status_code == 200
    assert response.content == b"fake_wav_header_and_data"
    assert response.headers["content-type"] == "audio/wav"
    
    # Verify args
    args = mock_synthesizer.synthesize.call_args[0][0]
    assert args.text == "こんにちは"
    assert args.style == "Happy"

def test_synthesize_stream_success(mock_synthesizer):
    # Setup mock generator for streaming
    async def fake_generator(request):
        yield b"chunk1"
        yield b"chunk2"

    mock_synthesizer.synthesize_stream = fake_generator
    
    payload = {
        "text": "Streaming test",
        "stream": True
    }
    
    response = client.post(
        "/api/v1/tts/synthesize",
        json=payload,
        headers={"X-API-Key": "test_secret"}
    )
    
    assert response.status_code == 200
    # Verify chunks are received (TestClient concatenates streaming response content usually)
    assert b"chunk1" in response.content
    assert b"chunk2" in response.content

def test_validation_error_speed():
    payload = {
        "text": "Too fast",
        "speed": 5.0 # Max is 2.0
    }
    response = client.post(
        "/api/v1/tts/synthesize",
        json=payload,
        headers={"X-API-Key": "test_secret"}
    )
    assert response.status_code == 422

def test_auth_missing():
    response = client.post(
        "/api/v1/tts/synthesize",
        json={"text": "No auth"},
        # No headers
    )
    assert response.status_code == 403