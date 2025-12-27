import asyncio
import logging
import time
from typing import AsyncGenerator

from backend.src.core.tts.model_manager import ModelManager
from backend.src.models.tts import TTSRequest
from backend.src.utils.audio import create_wav_header
from prometheus_client import Counter, Histogram

logger = logging.getLogger(__name__)

TTS_CHARS_TOTAL = Counter('tts_generated_characters_total', 'Total Japanese characters synthesized', ['model_id'])
TTS_INFERENCE_TIME = Histogram('tts_inference_duration_seconds', 'Time spent in TTS inference', ['model_id'])

class Synthesizer:
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        # Limit concurrent heavy inference tasks
        self._semaphore = asyncio.Semaphore(2)

    async def synthesize(self, request: TTSRequest) -> bytes:
        """
        Synthesizes text to audio and returns the full WAV bytes.
        """
        model_id = request.model_id or "default"
        async with self._semaphore:
            model = self.model_manager.load_model(model_id)
            
            start_time = time.perf_counter()
            logger.info(f"Synthesizing text: {request.text[:20]}... with model {model_id}")

            # Run inference in a threadpool to avoid blocking the event loop
            # style-bert-vits2 infer method returns (sr, audio_numpy_array) usually
            sr, audio_data = await asyncio.to_thread(
                model.infer,
                text=request.text,
                style=request.style,
                style_weight=request.style_weight,
                speed=request.speed,
                pitch=request.pitch
            )
            
            duration = time.perf_counter() - start_time
            TTS_INFERENCE_TIME.labels(model_id=model_id).observe(duration)
            TTS_CHARS_TOTAL.labels(model_id=model_id).inc(len(request.text))
            
            logger.info(
                "TTS Synthesis Complete",
                extra={
                    "text_len": len(request.text),
                    "duration": duration,
                    "model_id": model_id
                }
            )

            # Convert numpy array to WAV bytes
            # We assume audio_data is float32 or int16.
            # Style-Bert-VITS2 usually returns float32 or int16 numpy array.
            # We need to convert to bytes.
            
            import numpy as np
            
            # Normalize if float
            if audio_data.dtype.kind == 'f':
                # clip to -1.0, 1.0 and convert to int16
                audio_data = np.clip(audio_data, -1.0, 1.0)
                audio_data = (audio_data * 32767).astype(np.int16)
            
            raw_bytes = audio_data.tobytes()
            
            header = create_wav_header(
                sample_rate=sr,
                channels=1,
                bit_depth=16,
                data_size=len(raw_bytes)
            )
            
            return header + raw_bytes

    async def synthesize_stream(self, request: TTSRequest) -> AsyncGenerator[bytes, None]:
        """
        Streams audio chunks.
        """
        # Placeholder for streaming logic.
        # Style-Bert-VITS2 might support sentence-level streaming.
        # For now, we might just synthesize fully and yield chunked (if model doesn't support stream)
        # Or implement true streaming if the library exposes a generator.
        
        # MVP: Full synthesis then chunked yield (simulated stream) if library doesn't support streaming easily
        # But for "Time to First Byte", we need true streaming.
        # Let's assume we can split text and synthesize parts.
        
        full_audio = await self.synthesize(request)
        chunk_size = 4096
        for i in range(0, len(full_audio), chunk_size):
            yield full_audio[i:i+chunk_size]
            await asyncio.sleep(0.01) # Yield control
