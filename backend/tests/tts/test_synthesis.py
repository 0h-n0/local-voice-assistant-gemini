from unittest.mock import MagicMock

import numpy as np
import pytest
from backend.src.core.tts.synthesizer import Synthesizer
from backend.src.models.tts import TTSRequest


@pytest.mark.asyncio
async def test_synthesize_params():
    mock_manager = MagicMock()
    mock_model = MagicMock()
    
    # infer returns (sr, audio_data)
    # mock audio data as numpy array
    mock_audio = np.array([0, 1], dtype=np.int16)
    mock_model.infer = MagicMock(return_value=(44100, mock_audio))
    
    mock_manager.load_model.return_value = mock_model
    
    synth = Synthesizer(mock_manager)
    
    req = TTSRequest(
        text="Testing params",
        style="Sad",
        style_weight=0.5,
        speed=1.2,
        pitch=0.9
    )
    
    await synth.synthesize(req)
    
    mock_model.infer.assert_called_once()
    call_kwargs = mock_model.infer.call_args.kwargs
    
    assert call_kwargs['text'] == "Testing params"
    assert call_kwargs['style'] == "Sad"
    assert call_kwargs['style_weight'] == 0.5
    assert call_kwargs['speed'] == 1.2
    assert call_kwargs['pitch'] == 0.9 # Uncomment when supported
