import asyncio
import json
import os
import sys

import websockets
from dotenv import load_dotenv

# Add src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

async def main():
    load_dotenv()
    api_key = os.getenv("API_KEY", "test_key")
    uri = f"ws://localhost:8000/api/v1/orchestrator/ws?api_key={api_key}"

    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected. Type 'config' to send config, 'audio' to send dummy audio, or 'quit' to exit.")
            
            async def receive_messages():
                try:
                    async for message in websocket:
                        if isinstance(message, str):
                            print(f"\n[Server Event]: {message}")
                        else:
                            print(".", end="", flush=True) # Binary audio chunk
                except websockets.ConnectionClosed:
                    print("\nConnection closed by server.")

            asyncio.create_task(receive_messages())

            while True:
                cmd = await asyncio.get_event_loop().run_in_executor(None, input, "Command: ")
                if cmd == "quit":
                    break
                elif cmd == "config":
                    config = {
                        "type": "config",
                        "payload": {
                            "tts_voice": "Standard",
                            "tts_style": "Neutral"
                        }
                    }
                    await websocket.send(json.dumps(config))
                    print("Config sent.")
                elif cmd == "audio":
                    # Send a small dummy PCM chunk (silence)
                    dummy_audio = b"\x00" * 3200 # 0.1s of 16kHz 16-bit mono
                    await websocket.send(dummy_audio)
                    print("Dummy audio sent.")
                else:
                    print("Unknown command.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
