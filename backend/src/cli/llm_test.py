import asyncio
import os
import sys

from dotenv import load_dotenv

# Add src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.llm.service import llm_service
from src.models.llm import ChatMessage, LLMRequest


async def main():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment.")
        return

    prompt = input("Enter prompt: ")
    request = LLMRequest(
        messages=[ChatMessage(role="user", content=prompt)],
        stream=True
    )

    print("\nAssistant: ", end="", flush=True)
    async for chunk in llm_service.stream_chat_completion(request):
        print(chunk, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
