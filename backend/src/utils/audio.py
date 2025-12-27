import struct


def create_wav_header(sample_rate: int, channels: int = 1, bit_depth: int = 16, data_size: int = 0xFFFFFFFF) -> bytes:
    """
    Creates a valid RIFF WAV header.
    
    Args:
        sample_rate: Sampling frequency (e.g., 44100, 24000).
        channels: Number of channels (1 for mono, 2 for stereo).
        bit_depth: Bits per sample (e.g., 16).
        data_size: Total size of the audio data in bytes.
                   If unknown (streaming), use 0xFFFFFFFF or a placeholder.
    
    Returns:
        The 44-byte WAV header.
    """
    audio_format = 1  # PCM
    byte_rate = sample_rate * channels * bit_depth // 8
    block_align = channels * bit_depth // 8
    
    # If data_size is max uint32, we prevent overflow in ChunkSize
    chunk_size = 36 + data_size if data_size != 0xFFFFFFFF else 0xFFFFFFFF

    return struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        chunk_size,     # ChunkSize (36 + Subchunk2Size)
        b'WAVE',
        b'fmt ',
        16,             # Subchunk1Size for PCM
        audio_format,
        channels,
        sample_rate,
        byte_rate,
        block_align,
        bit_depth,
        b'data',
        data_size       # Subchunk2Size
    )
