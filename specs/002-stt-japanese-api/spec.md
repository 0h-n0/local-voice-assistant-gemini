# Feature Specification: Japanese STT API with ReazonSpeech

**Feature Branch**: `002-stt-japanese-api`  
**Created**: 2025-12-25
**Status**: Draft  
**Input**: User description: "reazon-research/reazonspeech-nemo-v2 を用いて音声ファイルまたはマイク入力から日本語テキストを生成する STT API を実装したい。"

## Clarifications

### Session 2025-12-25
- Q: What is the maximum size (in MB) for an audio file that can be directly uploaded to the /transcribe/file endpoint? → A: 50 MB.
- Q: What is the desired output format and content for the streaming transcription results? → A: Partial and final results with timestamps: Send JSON objects with partial transcriptions as they are recognized, and a final transcription for each segment, including timestamps.
- Q: What are the authentication and authorization requirements for accessing the STT API endpoints? → A: API Key: Access to API endpoints will require a valid API key sent in the request header or query parameter.
- Q: What level of observability (logging and/or metrics) is required for the STT API endpoints to ensure operational readiness? → A: Basic Observability: Structured logging for API requests/responses (e.g., endpoint, status code, duration, audio length) and basic Prometheus-compatible metrics (e.g., request count, error rate).
- Q: Should rate limiting be implemented for the API endpoints, and if so, what are the initial limits? → A: Basic Rate Limiting: Limit requests per IP address or API Key (e.g., 60 requests per minute per client).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Transcribe Audio File (Priority: P1)

As a user, I want to upload a Japanese audio file to the API so that I can receive its text transcription.

**Why this priority**: Transcribing pre-recorded audio is a fundamental and common use case for STT systems.

**Independent Test**: An API call with a Japanese audio file returns the correct text transcription.

**Acceptance Scenarios**:

1. **Given** a valid Japanese audio file (e.g., WAV, MP3) and the STT API is running, **When** I send a POST request with the audio file to the `/transcribe/file` endpoint, **Then** I receive a JSON response containing the Japanese text transcription.
2. **Given** an invalid audio file format, **When** I send a POST request to the `/transcribe/file` endpoint, **Then** the API returns an error indicating an unsupported format.
3. **Given** a Japanese audio file with speech, **When** I send a POST request, **Then** the returned text transcription is accurate.

---

### User Story 2 - Transcribe Live Microphone Input (Priority: P2)

As a user, I want to stream live Japanese audio input from a microphone to the API so that I can receive continuous text transcriptions.

**Why this priority**: Live transcription enables interactive applications like voice assistants or real-time captioning.

**Independent Test**: Streaming audio to the API results in a continuous output of transcribed text.

**Acceptance Scenarios**:

1. **Given** a connected microphone and the STT API is running, **When** I open a WebSocket connection and stream Japanese audio to the `/transcribe/stream` endpoint, **Then** the API continuously sends back JSON responses containing segments of Japanese text transcription.
2. **Given** a continuous audio stream with speech, **When** the API receives the audio, **Then** the API provides real-time transcription updates.
3. **Given** no audio is detected in the stream for a period, **When** the API receives the silent stream, **Then** the API does not send transcription updates or indicates silence.

---

### Edge Cases

- What happens if the audio file contains multiple languages or non-speech audio? (Assumption: The system will primarily focus on Japanese speech; non-Japanese or non-speech will either be ignored or result in less accurate transcription.)
- How does the system handle very long audio files (e.g., >1 hour)? (Assumption: Initial implementation will support files up to a certain length, with longer files potentially requiring batch processing.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The API MUST expose a `/transcribe/file` endpoint that accepts audio file uploads.
- **FR-002**: The `/transcribe/file` endpoint MUST support audio formats including WAV and MP3.
- **FR-003**: The `/transcribe/file` endpoint MUST return a JSON object containing the full Japanese text transcription.
- **FR-004**: The API MUST expose a `/transcribe/stream` endpoint that accepts live audio input via WebSocket.
- **FR-005**: The `/transcribe/stream` endpoint MUST continuously return JSON objects containing partial and final Japanese text transcriptions with timestamps for detected speech segments.
- **FR-006**: The API MUST utilize the `reazon-research/reazonspeech-nemo-v2` model for all Japanese speech-to-text conversions.
- **FR-007**: The API MUST handle errors gracefully for invalid audio inputs (e.g., unsupported format, corrupt file, no speech detected).
- **FR-008**: The `/transcribe/file` endpoint MUST enforce a maximum audio file upload size of 50 MB.
- **FR-009**: All API endpoints MUST require authentication via an API Key provided in the request header or query parameter.
- **FR-010**: The API MUST implement structured logging for key API request/response events (endpoint, status code, duration, audio length).
- **FR-011**: The API MUST expose basic Prometheus-compatible metrics (e.g., request count, error rate).
- **FR-012**: The API MUST implement basic rate limiting per IP address or API Key (e.g., 60 requests per minute per client).

### Key Entities *(include if feature involves data)*

- **AudioInput**:
  - `type`: (file, stream)
  - `data`: Binary audio data
  - `format`: (WAV, MP3, etc.)
- **TranscriptionResult**:
  - `text`: Japanese text transcription
  - `confidence`: (Optional) Confidence score of the transcription
  - `is_final`: Boolean, indicates if the transcription segment is final
  - `start_timestamp`: Float, start time of the speech segment in seconds
  - `end_timestamp`: Float, end time of the speech segment in seconds

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For audio files up to 30 seconds, the API MUST return a transcription within 5 seconds with a Word Error Rate (WER) of 10% or less for clear Japanese speech.
- **SC-002**: For live streaming audio, the API MUST achieve an end-to-end latency of less than 500ms (time from speech utterance to transcription segment display) with a WER of 15% or less for clear Japanese speech.
- **SC-003**: The API MUST successfully process 5 concurrent audio file transcription requests without exceeding the specified latency (SC-001) or returning errors.
- **SC-004**: The API MUST be able to process continuous audio streams for at least 1 hour without interruption or significant degradation in transcription quality.
