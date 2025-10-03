import asyncio

class LLMClient:
    async def generate(self, prompt: str) -> str:
        # Replace with OpenAI/HF API call
        await asyncio.sleep(0.2)  # simulate network latency
        return f"Summary based on: {prompt[:50]}..."

def get_llm_client():
    return LLMClient()