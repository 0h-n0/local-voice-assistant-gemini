# WebSocket Protocol: Voice Orchestrator

Endpoint: `ws://<host>:<port>/api/v1/orchestrator/ws`

## Message Types

The protocol uses interleaved Text (JSON) and Binary (PCM) frames.

### 1. Client -> Server (Upstream)

#### Configuration (JSON)
Sent immediately after connection.
```json
{
  "type": "config",
  "payload": {
    "tts_voice": "Airi",
    "tts_style": "Happy"
  }
}
```

#### Audio Data (Binary)
Chunks of raw 16kHz, 16-bit PCM (Mono) audio. Sent only when client VAD detects speech.

#### Speech Start (JSON)
Sent by client VAD to signal barge-in.
```json
{
  "type": "speech_start"
}
```

### 2. Server -> Client (Downstream)

#### Processing Started (JSON)
Sent when STT completes and LLM begins.
```json
{
  "type": "processing_start",
  "payload": {
    "transcript": "こんにちは"
  }
}
```

#### Audio Response (Binary)
Chunks of raw 16kHz, 16-bit PCM (Mono) synthesized audio.

#### Error (JSON)
```json
{
  "type": "error",
  "payload": {
    "code": "STT_FAILED",
    "message": "Speech to text conversion failed."
  }
}
```
