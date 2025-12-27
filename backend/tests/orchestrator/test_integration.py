import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

# Set API key for testing
os.environ["API_KEY"] = "test_key"

client = TestClient(app)

def test_websocket_orchestrator():
    # Mock the orchestrator instance used by the endpoint
    with patch("src.api.v1.endpoints.orchestrator.orchestrator") as mock_orchestrator:
        async def mock_process(*args, **kwargs):
            yield {"type": "processing_start", "payload": {"transcript": "input"}}
            yield b"audio_chunk"
            
        mock_orchestrator.process_audio_turn = mock_process
        
        with client.websocket_connect("/api/v1/orchestrator/ws?api_key=test_key") as websocket:
            # Send config
            websocket.send_json({"type": "config", "payload": {"tts_voice": "Airi"}})
            
            # Send audio bytes
            websocket.send_bytes(b"fake_audio")
            
            # Receive processing start
            resp = websocket.receive_json()
            assert resp["type"] == "processing_start"
            
            # Receive audio chunk
            resp = websocket.receive_bytes()
            assert resp == b"audio_chunk"
