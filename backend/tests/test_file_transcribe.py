import io
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import soundfile as sf
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi_limiter import FastAPILimiter  # Import FastAPILimiter

from src.api.v1.dependencies import get_api_key
from src.core.stt_processor import STTProcessor  # Import the class directly for patching
from src.main import app


# Override API key dependency for testing
def override_get_api_key():
    return "test_api_key"

app.dependency_overrides[get_api_key] = override_get_api_key

client = TestClient(app)

# --- Test Data ---
def create_dummy_audio(filename="dummy_audio.wav", duration_seconds=1, sr=16000, channels=1, subtype='PCM_16'):
    """Creates a dummy WAV file in memory."""
    t = np.linspace(0, duration_seconds, int(duration_seconds * sr), False)
    data = 0.5 * np.sin(2 * np.pi * 440 * t) # 440 Hz sine wave
    data = data.astype(np.float32)

    buffer = io.BytesIO()
    sf.write(buffer, data, sr, format='WAV', subtype=subtype) # Explicitly specify format
    buffer.seek(0)
    return buffer, filename

def create_large_dummy_audio(filename="large_dummy_audio.wav", size_mb=60, sr=16000, channels=1, subtype='PCM_16'):
    """Creates a dummy WAV file in memory exceeding 50MB."""
    bytes_per_second = sr * channels * (16 / 8) # 16-bit PCM
    duration_seconds = (size_mb * 1024 * 1024) / bytes_per_second
    return create_dummy_audio(filename, duration_seconds, sr, channels, subtype)

# --- Tests ---
@pytest.fixture(autouse=True, scope="session")
def mock_stt_processor_singleton_and_init(monkeypatch):
    """Mocks the STTProcessor class and its singleton instance to prevent actual model loading.
    This fixture runs once per test session.
    """
    mock_instance = MagicMock(spec=STTProcessor)
    mock_instance.transcribe.return_value = "これはテストの文字起こしです"

    async def mock_transcribe_stream_async_generator(*args, **kwargs):
        yield {"text": "ストリーミングモック", "is_final": False, "start_timestamp": 0.0, "end_timestamp": 0.5}
        yield {"text": "最終結果", "is_final": True, "start_timestamp": 0.5, "end_timestamp": 1.0}

    mock_instance.transcribe_stream.return_value = mock_transcribe_stream_async_generator()

    # Patch the STTProcessor class itself so that STTProcessor() returns our mock instance
    monkeypatch.setattr('src.core.stt_processor.STTProcessor', MagicMock(return_value=mock_instance))

    # Also patch the module-level singleton instance if it's already created
    monkeypatch.setattr('src.core.stt_processor.stt_processor', mock_instance)

    # Mock FastAPILimiter.init to prevent it from trying to connect to Redis during tests
    monkeypatch.setattr(FastAPILimiter, 'init', MagicMock(return_value=None))
    # Mock the redis_client itself in rate_limiter.py
    monkeypatch.setattr('src.middlewares.rate_limiter.redis_client', MagicMock())

    return mock_instance

@pytest.fixture(autouse=True)
def setup_env_vars(monkeypatch):
    """Sets up environment variables for tests.
    """
    # Set a test API key for the environment
    monkeypatch.setenv("API_KEY", "test_api_key")
    yield # Run the tests
    # Teardown
    monkeypatch.delenv("API_KEY", raising=False) # Clean up env var


def test_successful_file_transcription(mock_stt_processor_singleton_and_init):
    # The stt_processor.transcribe method is already mocked globally by mock_stt_processor_singleton fixture
    audio_buffer, filename = create_dummy_audio()
    response = client.post(
        "/api/v1/transcribe/file",
        headers={"X-API-Key": "test_api_key"},
        files={"audio_file": (filename, audio_buffer, "audio/wav")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "text": "これはテストの文字起こしです",
        "confidence": None, # Assuming None for now, model might provide
        "is_final": True,
        "start_timestamp": 0.0,
        "end_timestamp": 1.0 # Dummy value, will be actual from model
    }
    mock_stt_processor_singleton_and_init.transcribe.assert_called_once()


def test_missing_api_key(monkeypatch):
    audio_buffer, filename = create_dummy_audio()
    # Temporarily remove API_KEY env var for this test
    monkeypatch.delenv("API_KEY", raising=False) # Use monkeypatch to manage env var safely
    response = client.post(
        "/api/v1/transcribe/file",
        files={"audio_file": (filename, audio_buffer, "audio/wav")}
    )
    assert response.status_code == 403
    assert "Could not validate credentials" in response.json()["detail"]


def test_invalid_api_key():
    audio_buffer, filename = create_dummy_audio()
    response = client.post(
        "/api/v1/transcribe/file",
        headers={"X-API-Key": "wrong_key"},
        files={"audio_file": (filename, audio_buffer, "audio/wav")}
    )
    assert response.status_code == 403
    assert "Could not validate credentials" in response.json()["detail"]

def test_unsupported_audio_format():
    audio_buffer = io.BytesIO(b"dummy_data") # Not a real audio file
    response = client.post(
        "/api/v1/transcribe/file",
        headers={"X-API-Key": "test_api_key"},
        files={"audio_file": ("dummy.txt", audio_buffer, "text/plain")} # Incorrect MIME type
    )
    assert response.status_code == 400
    assert "Unsupported media type" in response.json()["detail"]

def test_file_size_exceeds_limit(mock_stt_processor_singleton_and_init):
    large_audio_buffer, filename = create_large_dummy_audio()

    # This test currently relies on actual implementation of file size check in the endpoint
    response = client.post(
        "/api/v1/transcribe/file",
        headers={"X-API-Key": "test_api_key"},
        files={"audio_file": (filename, large_audio_buffer, "audio/wav")}
    )
    assert response.status_code == 400
    assert "File size exceeds 50MB limit" in response.json()["detail"]
    mock_stt_processor_singleton_and_init.transcribe.assert_not_called() # Transcription should not be attempted

# Rate limiting test requires actual rate limiter to be initialized
# For this test, we need to mock FastAPI-Limiter or set up a test Redis.
# This will be integrated in a later stage when FastAPILimiter is fully configured.
@patch('src.middlewares.rate_limiter.FastAPILimiter.redis') # Patch the redis client to be a mock
def test_rate_limiting(mock_redis, mock_stt_processor_singleton_and_init):
    mock_redis.get.return_value = None # No previous calls
    mock_redis.setex.return_value = None # Set the key

    # Mock the actual rate limit check within the dependency
    with patch('src.middlewares.rate_limiter.RateLimiter.__call__') as mock_ratelimiter_call:
        mock_ratelimiter_call.side_effect = HTTPException(status_code=429, detail="Rate limit exceeded")
        audio_buffer, filename = create_dummy_audio()

        response = client.post(
            "/api/v1/transcribe/file",
            headers={"X-API-Key": "test_api_key"},
            files={"audio_file": (filename, audio_buffer, "audio/wav")}
        )
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["detail"]
