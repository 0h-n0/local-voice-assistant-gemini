import asyncio
import logging
import re
import time
from typing import AsyncGenerator, List, Tuple

import numpy as np
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

    def _split_sentences(self, text: str) -> List[str]:
        """
        Splits Japanese text into sentences to reduce latency for streaming.
        Splits by `。`, `！`, `？`, `\n` and keeps the delimiters.
        """
        # Finds one or more non-delimiter characters followed by optional delimiters
        # This keeps the punctuation attached to the sentence.
        sentences = re.findall(r'[^。！？\n]+[。！？\n]*', text)
        if not sentences:
            return [text] if text else []
        return sentences

    async def _infer_pcm(self, text: str, request: TTSRequest) -> Tuple[int, bytes]:
        """
        Internal method to run inference and return (sample_rate, pcm_bytes).
        """
        model_id = request.model_id or "default"
        
        # Load model (outside semaphore to allow caching check, but load is fast if cached)
        # However, accessing model object inside semaphore is safer if not thread-safe.
        # model_manager.load_model is thread-safe enough for read.
        
        async with self._semaphore:
            model = self.model_manager.load_model(model_id)
            
            start_time = time.perf_counter()
            logger.debug(f"Inferring segment: {text[:10]}... (model: {model_id})")

            # Run inference in a threadpool
            sr, audio_data = await asyncio.to_thread(
                model.infer,
                text=text,
                style=request.style,
                style_weight=request.style_weight,
                speed=request.speed,
                pitch=request.pitch
            )
            
            duration = time.perf_counter() - start_time
            TTS_INFERENCE_TIME.labels(model_id=model_id).observe(duration)
            TTS_CHARS_TOTAL.labels(model_id=model_id).inc(len(text))

            # Normalize if float
            if audio_data.dtype.kind == 'f':
                audio_data = np.clip(audio_data, -1.0, 1.0)
                audio_data = (audio_data * 32767).astype(np.int16)
            
            return sr, audio_data.tobytes()

    async def synthesize(self, request: TTSRequest) -> bytes:
        """
        Synthesizes full text to audio (WAV) in one go (Batch mode).
        """
        model_id = request.model_id or "default"
        logger.info(f"Batch synthesis start: {len(request.text)} chars (model: {model_id})")
        
        sr, pcm_data = await self._infer_pcm(request.text, request)
        
        header = create_wav_header(
            sample_rate=sr,
            channels=1,
            bit_depth=16,
            data_size=len(pcm_data)
        )
        
        return header + pcm_data

    async def synthesize_stream(self, request: TTSRequest) -> AsyncGenerator[bytes, None]:
        """
        Streams audio chunks by synthesizing sentence by sentence (True Streaming).
        """
        sentences = self._split_sentences(request.text)
        logger.info(f"Streaming synthesis start: {len(request.text)} chars, {len(sentences)} segments")
        
        first_chunk = True
        
        for segment in sentences:
            if not segment.strip():
                continue
                
            try:
                sr, pcm_data = await self._infer_pcm(segment, request)
                
                if first_chunk:
                    # Send WAV header with unknown size (0xFFFFFFFF)
                    yield create_wav_header(
                        sample_rate=sr,
                        channels=1,
                        bit_depth=16,
                        data_size=0xFFFFFFFF
                    )
                    first_chunk = False
                
                yield pcm_data
                
            except Exception as e:
                logger.error(f"Error synthesizing segment '{segment}': {e}")
                # Continue to next segment? or abort. Usually abort.
                raise e