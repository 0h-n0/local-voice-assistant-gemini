import argparse
import asyncio
import os
import sys

from dotenv import load_dotenv

# Add src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.tts.model_manager import ModelManager
from src.core.tts.synthesizer import Synthesizer
from src.models.tts import TTSRequest


async def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Japanese TTS CLI")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--out", "-o", default="output.wav", help="Output file path")
    parser.add_argument("--model", help="Model ID")
    parser.add_argument("--style", default="Neutral", help="Style/Emotion")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed")
    parser.add_argument("--pitch", type=float, default=1.0, help="Pitch")
    
    args = parser.parse_args()
    
    print(f"Synthesizing: '{args.text}' (Style: {args.style}, Speed: {args.speed})")
    
    manager = ModelManager()
    synth = Synthesizer(manager)
    
    req = TTSRequest(
        text=args.text,
        model_id=args.model,
        style=args.style,
        speed=args.speed,
        pitch=args.pitch
    )
    
    try:
        audio_data = await synth.synthesize(req)
        with open(args.out, "wb") as f:
            f.write(audio_data)
        print(f"Success! Saved to {args.out}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
