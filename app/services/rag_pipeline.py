from app.core.prompts import SUMMARY_PROMPT

class RAGPipeline:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    async def run(self, query: str, top_k: int = 5):
        docs = self.retriever.search(query, top_k)
        context = "\n\n".join([d["text"] for d in docs])
        prompt = SUMMARY_PROMPT.format(context=context, query=query)
        summary = await self.llm.generate(prompt)
        return {"summary": summary, "retrieved_docs": docs}