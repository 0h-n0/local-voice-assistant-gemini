"""OpenAI client wrapper."""
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

class OpenAIClient:
    """Wrapper for OpenAI AsyncOpenAI client."""
    def __init__(self):
        """Initialize the client with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-5-mini"

    async def create_chat_completion(self, messages, temperature=1.0, max_tokens=None, stream=False):
        """Create a chat completion using the OpenAI API."""
        return await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )

openai_client = OpenAIClient()