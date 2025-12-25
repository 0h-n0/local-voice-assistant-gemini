from nemo.collections.asr.models import ASRModel
import logging
import os
import tempfile

logger = logging.getLogger(__name__)

class STTProcessor:
    _instance = None
    _model: ASRModel = None # Initialize to None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(STTProcessor, cls).__new__(cls)
            # Do NOT call _load_model here. Model will be loaded lazily.
        return cls._instance

    def _load_model_if_needed(self):
        """
        Loads the reazonspeech-nemo-v2 model if it hasn't been loaded yet.
        """
        if self._model is None:
            logger.info("Lazily loading reazonspeech-nemo-v2 model...")
            try:
                # Assuming the model can be loaded from pretrained
                self._model = ASRModel.from_pretrained(model_name="reazonspeech-nemo-v2")
                logger.info("reazonspeech-nemo-v2 model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load reazonspeech-nemo-v2 model: {e}")
                raise

    def transcribe(self, audio_bytes: bytes) -> str:
        """
        Transcribes given audio bytes (expected to be in WAV format).
        """
        self._load_model_if_needed() # Ensure model is loaded before transcribing
        
        if self._model is None:
            raise RuntimeError("STT model not loaded.")
        
        # Write audio bytes to a temporary WAV file for NeMo to process
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_file_path = temp_audio_file.name
            
            try:
                hypotheses = self._model.transcribe(paths2audio_files=[temp_audio_file_path])
                return hypotheses[0] if hypotheses else ""
            except Exception as e:
                logger.error(f"Error during transcription: {e}")
                raise

    async def transcribe_stream(self, audio_chunk_generator):
        """
        Placeholder for streaming transcription.
        This would involve a more complex interaction with Nemo's streaming API.
        """
        self._load_model_if_needed() # Ensure model is loaded before streaming transcription
        logger.info("Simulating streaming transcription...")
        yield {"text": "ストリーミング転写のシミュレーション", "is_final": False, "start_timestamp": 0.0, "end_timestamp": 1.0}
        yield {"text": "これは最終的な結果です", "is_final": True, "start_timestamp": 1.0, "end_timestamp": 2.5}

stt_processor = STTProcessor()