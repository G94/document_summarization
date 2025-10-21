import asyncio
from langchain_openai import OpenAI
from app.core.config import OPENAI_API_KEY, LLM_NAME

class LLMClient:
    def __init__(self):
        self.llm=OpenAI(
            model=LLM_NAME,
            temperature=0,
            max_retries=2,
            api_key=str(OPENAI_API_KEY),  # Replace with your actual OpenAI API key or set as environment variable
        )

    async def generate(self, prompt: str) -> str:
        # Replace with OpenAI/HF API call
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.llm.invoke, prompt)
        return response

def get_llm_client():
    return LLMClient()