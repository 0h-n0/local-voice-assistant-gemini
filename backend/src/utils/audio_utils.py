import io

import pydub


def convert_audio_to_wav(audio_bytes: bytes, original_format: str) -> bytes:
    """Converts audio from its original format to WAV (PCM, 16kHz, mono, 16-bit).
    """
    audio_segment = pydub.AudioSegment.from_file(io.BytesIO(audio_bytes), format=original_format)

    # Set frame rate, channels, and sample width for Nemo compatibility
    audio_segment = audio_segment.set_frame_rate(16000)
    audio_segment = audio_segment.set_channels(1)
    audio_segment = audio_segment.set_sample_width(2) # 16-bit

    output_buffer = io.BytesIO()
    audio_segment.export(output_buffer, format="wav")
    return output_buffer.getvalue()

def get_audio_duration(audio_bytes: bytes, audio_format: str) -> float:
    """Gets the duration of audio in seconds.
    """
    audio_segment = pydub.AudioSegment.from_file(io.BytesIO(audio_bytes), format=audio_format)
    return len(audio_segment) / 1000.0

def chunk_audio(audio_bytes: bytes, chunk_size_ms: int = 1000) -> bytes:
    """Chunks audio into smaller pieces for streaming.
    (Placeholder - actual streaming would involve more complex buffering/processing)
    """
    # This is a simplification. Real-time streaming would require
    # more advanced buffering and non-blocking I/O.
    # For now, it just returns the whole audio.
    return audio_bytes
