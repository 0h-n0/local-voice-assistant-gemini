# Data Model: Japanese TTS API

This document defines the entities used in the TTS service.

## Entities

### TTSRequest
Input parameters for voice synthesis.
- `text`: String (max 500 characters) - The Japanese text to synthesize.
- `model_id`: String (optional) - The specific model/speaker to use.
- `style`: String (optional, default: "Neutral") - The emotion/style name.
- `style_weight`: Float (optional, default: 1.0) - Intensity of the chosen style.
- `speed`: Float (range: 0.5 - 2.0, default: 1.0) - Speech rate.
- `pitch`: Float (default: 1.0) - Fundamental frequency scale.
- `stream`: Boolean (default: false) - Whether to use chunked transfer encoding.

### VoiceModel
Information about an available TTS model.
- `id`: String - Unique identifier.
- `name`: String - Human-readable name.
- `styles`: List[String] - List of supported emotion style names.
- `sample_rate`: Integer - Default output sample rate (e.g., 44100).

### AudioMetadata
Metadata returned in headers or along with the batch file.
- `format`: String ("wav")
- `sample_rate`: Integer
- `duration`: Float (seconds) - Calculated post-synthesis.
