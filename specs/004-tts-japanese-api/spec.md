# Feature Specification: Japanese TTS API with Style-Bert-VITS2

**Feature Branch**: `004-tts-japanese-api`  
**Created**: 2025-12-25  
**Status**: Draft  
**Input**: User description: "Style-Bert-VITS2 を用いて日本語テキストを自然音声に変換する TTS API を実装したい。"

## Clarifications

### Session 2025-12-25
- Q: Should the API support streaming the audio data as it is generated, or is a standard batch file response sufficient? → A: Both. The system must support both full WAV file responses and chunked streaming responses, selectable by the caller.
- Q: What are the authentication requirements for accessing the TTS API endpoints? → A: API Key: Access requires a valid API key passed in the request header or query parameter.
- Q: What level of observability (logging/metrics) should be implemented for the TTS API? → A: Basic Observability: Structured JSON logging for all requests and basic Prometheus-compatible metrics (request count, latency, error rate).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Voice Synthesis from Text (Priority: P1)

As a user of the assistant, I want to send Japanese text to the system and receive a high-quality audio response so that the assistant can "speak" to me.

**Why this priority**: This is the core functionality. Without basic synthesis, the feature provides no value.

**Independent Test**: Send a simple Japanese sentence ("こんにちは、調子はどうですか？") and verify that a valid WAV file is returned and contains audible speech.

**Acceptance Scenarios**:

1. **Given** a valid Japanese text string, **When** the TTS API is called in batch mode, **Then** it returns a binary audio stream (WAV format).
2. **Given** a valid Japanese text string, **When** the TTS API is called in streaming mode, **Then** it begins sending audio chunks immediately as they are generated.
3. **Given** an empty text input, **When** the TTS API is called, **Then** it returns a validation error (400 Bad Request).
4. **Given** a very long text string (exceeding 500 characters), **When** the TTS API is called, **Then** it returns an informative error about the character limit.

---

### User Story 2 - Style and Emotion Control (Priority: P2)

As a developer, I want to specify the "style" or "emotion" of the generated voice (e.g., Happy, Sad, Angry) so that the assistant's voice matches the context of the conversation.

**Why this priority**: Style-Bert-VITS2 is chosen specifically for its expressive capabilities. Controlling styles is a key feature of this model.

**Independent Test**: Generate two audio files from the same text, one with style "Happy" and one with "Sad", and verify (qualitatively) that the prosody differs.

**Acceptance Scenarios**:

1. **Given** a specific style parameter (e.g., `style="Happy"`), **When** the synthesis is requested, **Then** the generated audio reflects the requested emotion.
2. **Given** an unsupported style name, **When** requested, **Then** the system falls back to the "Neutral" style and provides a warning or success with default behavior.

---

### User Story 3 - Voice Parameter Tuning (Priority: P2)

As a developer, I want to adjust parameters like speed, pitch, and intonation scale so that I can fine-tune the delivery of the speech.

**Why this priority**: Essential for handle different types of content (e.g., reading a long article faster or emphasizing specific words).

**Independent Test**: Generate audio with `speed=2.0` and verify that the resulting duration is approximately half of the audio generated with `speed=1.0`.

**Acceptance Scenarios**:

1. **Given** custom `speed`, `pitch`, or `sdp_ratio` values, **When** requested, **Then** the synthesis engine applies these parameters to the output.

---

### Edge Cases

- **Special Characters**: Handling of Emoji, English words within Japanese text, and punctuation.
- **Concurrent Requests**: Behavior of the API when multiple synthesis requests arrive simultaneously (given GPU/CPU intensity).
- **Model Loading**: Behavior during the first request if the model is not yet loaded into memory.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an endpoint to accept Japanese text strings for synthesis.
- **FR-002**: System MUST return binary audio data in WAV format.
- **FR-003**: System MUST support selection of a specific model/speaker ID if multiple are available.
- **FR-004**: System MUST allow controlling the "Style" (Emotion) scale.
- **FR-005**: System MUST allow adjusting voice parameters: `speed` (0.5 to 2.0), `pitch`, and `style_weight`.
- **FR-006**: System MUST support both batch (full file) and streaming (chunked transfer encoding) responses, selectable by the caller.
- **FR-007**: System MUST validate input text length to prevent resource exhaustion.
- **FR-008**: All API endpoints MUST require authentication via an API Key provided in the request header or query parameter.
- **FR-009**: The system MUST implement structured JSON logging for all synthesis requests, including character count and synthesis duration.
- **FR-010**: The system MUST expose basic Prometheus-compatible metrics (request total, error total, latency histogram).

### Key Entities *(include if feature involves data)*

- **TTSRequest**: Input parameters including `text`, `model_id`, `style`, `speed`, `stream` (boolean), etc.
- **VoiceModel**: Metadata about available Style-Bert-VITS2 models (speakers, supported styles).
- **AudioOutput**: The resulting binary audio data and its metadata (sample rate, format).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Synthesis of a 20-character sentence is completed in under 2.0 seconds (Time to First Byte for streaming, or full file for batch).
- **SC-002**: Resulting audio has a sample rate of at least 44.1kHz (or model default, usually high-fidelity).
- **SC-003**: API supports at least 2 concurrent synthesis sessions without significant degradation in performance.
- **SC-004**: System handles at least 10 different styles/emotions as defined by the underlying model.
- **SC-005**: 100% of synthesis requests and their metadata are accurately tracked in structured logs.