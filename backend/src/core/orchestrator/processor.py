import asyncio
import logging
import re
import time
from typing import AsyncGenerator, Union

from src.core.orchestrator.session import SessionContext
from src.models.llm import ChatMessage as LLMChatMessage
from src.models.llm import LLMRequest
from src.models.tts import TTSRequest

logger = logging.getLogger(__name__)

class VoiceOrchestrator:
    def __init__(self, stt_service, llm_service, tts_service):
        self.stt_service = stt_service
        self.llm_service = llm_service
        self.tts_service = tts_service

    def _split_into_sentences(self, text: str) -> list[str]:
        # Split by Japanese punctuation
        return re.findall(r'[^。！？\n]+[。！？\n]*', text)

    async def process_audio_turn(self, audio_bytes: bytes, session: SessionContext) -> AsyncGenerator[Union[dict, bytes], None]:
        """
        Orchestrates one turn of voice interaction:
        1. STT: audio -> text
        2. LLM: text -> stream of tokens
        3. TTS: tokens -> sentence chunks -> audio stream
        """
        start_time = time.perf_counter()
        try:
            # 1. STT
            stt_start = time.perf_counter()
            transcript = await asyncio.to_thread(self.stt_service.transcribe, audio_bytes)
            stt_duration = time.perf_counter() - stt_start
            
            logger.info("STT stage complete", extra={
                "session_id": str(session.session_id),
                "duration": stt_duration,
                "stage": "stt"
            })

            if not transcript:
                yield {"type": "error", "payload": {"code": "NO_SPEECH", "message": "No speech detected"}}
                return

            session.add_message(role="user", content=transcript)
            yield {"type": "processing_start", "payload": {"transcript": transcript}}

            # 2. LLM
            llm_start = time.perf_counter()
            first_token_received = False
            
            # Convert session history to LLM messages
            messages = [LLMChatMessage(role=m.role, content=m.content) for m in session.history]
            llm_request = LLMRequest(messages=messages, stream=True)

            full_response = ""
            current_buffer = ""
            
            async for token in self.llm_service.stream_chat_completion(llm_request):
                if not first_token_received:
                    llm_ttfb = time.perf_counter() - llm_start
                    logger.info("LLM TTFB", extra={
                        "session_id": str(session.session_id),
                        "duration": llm_ttfb,
                        "stage": "llm_ttfb"
                    })
                    first_token_received = True
                
                full_response += token
                current_buffer += token
                
                # Check for sentence boundaries
                if any(p in token for p in "。！？\n"):
                    sentences = self._split_into_sentences(current_buffer)
                    # Process all but the last potentially incomplete sentence
                    for i in range(len(sentences) - 1):
                        sentence = sentences[i]
                        async for audio_chunk in self._stream_tts(sentence, session.config, session.session_id):
                            yield audio_chunk
                    current_buffer = sentences[-1]

            # Process remaining buffer
            if current_buffer.strip():
                async for audio_chunk in self._stream_tts(current_buffer, session.config, session.session_id):
                    yield audio_chunk

            session.add_message(role="assistant", content=full_response)
            
            total_duration = time.perf_counter() - start_time
            logger.info("Voice turn complete", extra={
                "session_id": str(session.session_id),
                "total_duration": total_duration,
                "chars_count": len(full_response)
            })

        except asyncio.CancelledError:
            logger.info("Voice turn processing cancelled", extra={"session_id": str(session.session_id)})
            raise
        except Exception as e:
            logger.error(f"Error in voice orchestrator: {e}", exc_info=True, extra={"session_id": str(session.session_id)})
            yield {"type": "error", "payload": {"code": "INTERNAL_ERROR", "message": str(e)}}

    async def _stream_tts(self, text: str, config, session_id) -> AsyncGenerator[bytes, None]:
        tts_start = time.perf_counter()
        tts_request = TTSRequest(
            text=text,
            model_id=config.tts_voice,
            style=config.tts_style,
            stream=True
        )
        first_chunk = True
        async for chunk in self.tts_service.synthesize_stream(tts_request):
            if first_chunk:
                tts_ttfb = time.perf_counter() - tts_start
                logger.info("TTS segment TTFB", extra={
                    "session_id": str(session_id),
                    "duration": tts_ttfb,
                    "text_len": len(text),
                    "stage": "tts_ttfb"
                })
                first_chunk = False
            yield chunk
