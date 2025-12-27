import logging
import os
from typing import Dict, List, Optional

from backend.src.models.tts import VoiceModel

logger = logging.getLogger(__name__)

# Conditional import to allow tests to run without the library installed
try:
    from style_bert_vits2.tts_model import TTSModel
except ImportError:
    TTSModel = None
    logger.warning("style_bert_vits2 library not found. TTS functionality will be limited.")

class ModelManager:
    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = model_dir or os.getenv("TTS_MODEL_DIR", "data/models/tts")
        self._loaded_models: Dict[str, object] = {} # object used if TTSModel is None
        self._model_info: Dict[str, VoiceModel] = {}

    def load_model(self, model_id: str) -> object:
        """
        Loads the model into memory if not already loaded.
        Returns the TTSModel instance.
        """
        if model_id in self._loaded_models:
            return self._loaded_models[model_id]

        if TTSModel is None:
            raise RuntimeError("style_bert_vits2 library is not installed.")

        model_path = os.path.join(self.model_dir, model_id)
        if not os.path.exists(model_path):
            raise ValueError(f"Model directory not found: {model_path}")

        # Standard file expectations for Style-Bert-VITS2
        safetensors_file = os.path.join(model_path, f"{model_id}.safetensors")
        config_file = os.path.join(model_path, "config.json")
        style_file = os.path.join(model_path, "style_vectors.npy")

        if not os.path.exists(safetensors_file):
             # Fallback: check for any safetensors or pth
             files = os.listdir(model_path)
             safetensors = [f for f in files if f.endswith(".safetensors")]
             if safetensors:
                 safetensors_file = os.path.join(model_path, safetensors[0])
             else:
                 raise ValueError(f"No model weights found in {model_path}")

        logger.info(f"Loading TTS model: {model_id}")
        
        # Determine device
        device = "cuda" if os.getenv("USE_GPU", "false").lower() == "true" else "cpu"

        model = TTSModel(
            model_path=safetensors_file,
            config_path=config_file,
            style_vec_path=style_file,
            device=device
        )
        
        self._loaded_models[model_id] = model
        
        # Cache model info
        styles = list(model.style2id.keys()) if hasattr(model, 'style2id') else ["Neutral"]
        sampling_rate = model.configs.data.sampling_rate if hasattr(model, 'configs') else 44100

        self._model_info[model_id] = VoiceModel(
            id=model_id,
            name=model_id,
            styles=styles,
            sample_rate=sampling_rate
        )
        
        return model

    def get_model_info(self, model_id: str) -> Optional[VoiceModel]:
        """Returns metadata for a loaded model."""
        return self._model_info.get(model_id)

    def list_models(self) -> List[VoiceModel]:
        """
        Scans the model directory and returns available models.
        Note: This is a lightweight scan. For full details (styles),
        the model usually needs to be loaded or config parsed.
        """
        models = []
        if not os.path.exists(self.model_dir):
            return models

        for name in os.listdir(self.model_dir):
            path = os.path.join(self.model_dir, name)
            if os.path.isdir(path):
                # If we have it loaded, return full info
                if name in self._model_info:
                    models.append(self._model_info[name])
                else:
                    # Basic info
                    models.append(VoiceModel(
                        id=name,
                        name=name,
                        styles=["(Load to see styles)"],
                        sample_rate=44100
                    ))
        return models
