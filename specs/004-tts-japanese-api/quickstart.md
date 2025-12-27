# Quickstart: Japanese TTS API

This service allows you to convert Japanese text into high-quality expressive speech using `Style-Bert-VITS2`.

## Prerequisites
- Python 3.11+
- Valid API Key (set in `.env`)

## Batch Synthesis
Returns a full WAV file once synthesis is complete.

```bash
curl -X POST http://localhost:8000/api/v1/tts/synthesize \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d 
    "{
    "text": "こんにちは、今日は良い天気ですね。",
    "style": "Happy",
    "speed": 1.1
  }" --output output.wav
```

## Streaming Synthesis
Begins returning audio chunks immediately (useful for perceived latency).

```bash
curl -X POST http://localhost:8000/api/v1/tts/synthesize \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d 
    "{
    "text": "非常に長い文章を読み上げるときは、ストリーミングモードを使用することをお勧めします。",
    "stream": true
  }" --no-buffer > stream_output.wav
```

## Available Models
Query the `/api/v1/tts/models` endpoint to see available speakers and their supported emotions.

