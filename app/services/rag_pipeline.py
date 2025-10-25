from core.prompts import SUMMARY_PROMPT, SUMMARY_PROMPT_DOC
from models.metrics import MetricEvaluator, BertScore, RougeScore

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
    
class SummaryPipeline:
    def __init__(self,  llm):
        self.llm = llm
        self.summary = ""

    async def run(self, text: str):
        prompt = SUMMARY_PROMPT_DOC.format(document_content=text)
        self.summary = await self.llm.generate(prompt)
        return {"summary": self.summary}
    
class EvaluationPipeline:
    def __init__(self):
        pass

    async def run(self, generated_text:str,  reference_text: str):
        # bertscore=BertScore.compute(reference=reference_text, prediction=generated_text)
        print(reference_text)
        print(generated_text)
        print("EvaluationPipeline")
        rougescore=RougeScore.computa(ref=reference_text, pred=generated_text)
        return [rougescore]