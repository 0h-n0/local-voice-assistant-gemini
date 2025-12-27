# Quickstart: Voice Interaction Orchestrator

The Orchestrator combines STT, LLM, and TTS into a single low-latency loop.

## Connection

Connect to the WebSocket endpoint:
`ws://localhost:8000/api/v1/orchestrator/ws?api_key=YOUR_API_KEY`

## Interaction Flow

1.  **Handshake**: Optionally send a `config` message.
2.  **Speak**: Send binary PCM audio chunks. The client should use VAD to only send audio during speech.
3.  **Barge-in**: If the server is currently sending audio and you wish to interrupt, send a `speech_start` JSON frame and immediately begin sending the new audio binary.
4.  **Listen**: Receive binary PCM chunks from the server and play them back.

## Example (Python Client)

```python
import websockets
import asyncio
import json

async def voice_chat():
    uri = "ws://localhost:8000/api/v1/orchestrator/ws?api_key=test_key"
    async with websockets.connect(uri) as ws:
        # 1. Send Config
        await ws.send(json.dumps({"type": "config", "payload": {"tts_voice": "Standard"}}))
        
        # 2. Send Audio (Placeholder)
        # with open("input.pcm", "rb") as f:
        #     await ws.send(f.read())
        
        # 3. Receive Response
        async for message in ws:
            if isinstance(message, str):
                print(f"Server Event: {message}")
            else:
                # Handle binary audio playback
                pass

asyncio.run(voice_chat())
```
