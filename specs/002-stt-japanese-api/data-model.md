# Data Model: Japanese STT API

This document defines the key entities involved in the Japanese STT API.

## AudioInput

Represents the input audio data, whether from a file upload or a real-time stream.

- `type`: String (Enum: `file`, `stream`)
  - Description: Indicates the source type of the audio.
- `data`: Binary
  - Description: The raw binary audio data.
- `format`: String (Enum: `WAV`, `MP3`, `PCM`, etc.)
  - Description: The format of the audio data.

## TranscriptionResult

Represents the result of a speech-to-text transcription. For streaming, this can include partial results.

- `text`: String
  - Description: The transcribed Japanese text.
- `confidence`: Float (Optional)
  - Description: A confidence score for the transcription, typically between 0.0 and 1.0.
- `is_final`: Boolean
  - Description: For streaming results, `true` if this is a final segment transcription, `false` for a partial/interim result.
- `start_timestamp`: Float
  - Description: The start time of the speech segment in seconds, relative to the audio start.
- `end_timestamp`: Float
  - Description: The end time of the speech segment in seconds, relative to the audio start.
