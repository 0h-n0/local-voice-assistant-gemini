from functools import lru_cache

from backend.src.core.tts.model_manager import ModelManager
from backend.src.core.tts.synthesizer import Synthesizer


@lru_cache()
def get_model_manager() -> ModelManager:
    return ModelManager()

@lru_cache()
def get_synthesizer() -> Synthesizer:
    # Synthesizer depends on ModelManager.
    # We resolve ModelManager here to ensure the singleton instance is passed.
    return Synthesizer(get_model_manager())
