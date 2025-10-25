from pydantic import BaseModel, Field
from typing import Optional, Union, List
from abc import ABC, abstractmethod
# import evaluate
# import inspect
from rouge import Rouge
# from evaluate import load
# rouge = evaluate.load("rouge", module_type="metric", download_mode="force_redownload")
# bertscore = evaluate.load("bertscore")

class MetricResult(BaseModel):
    name: str
    score: float

class MetricEvaluator(ABC):
    @abstractmethod
    def compute(prediction: str, reference: str) -> MetricResult:
        pass

class RougeScore:
    #@staticmethod
    def computa(pred: str, ref: str) -> MetricResult:
        generated_text="El Alzheimer es una enfermedad neurodegenerativa "
        reference_text="El Alzheimer es una enfermedad del cerebro que deteriora lentamente"
        # rouge = evaluate.load("rouge")
        rouge = Rouge()
        scores = rouge.get_scores(pred, ref)
        print(scores[0]['rouge-1']['r'])
        # print(rouge, inspect.signature(rouge.compute))
        # score = rouge.compute(predictions=[generated_text], other_arg=[reference_text])
        return MetricResult(name='ROUGE-L', score=scores[0]['rouge-1']['r'])

class BertScore:
    @staticmethod
    def compute(self, reference: str, prediction: str) -> MetricResult:
        # score = bertscore.compute(predictions=[prediction], references=[reference], lang="en")
        score= 0.0
        return MetricResult(name='BERTSCORE', score=score)
    
if __name__ == "__main__":
    pred = ["hello there", "general kenobi"]
    ref = ["hello there", "general kenobi"]
    result = rouge.compute(predictions=pred, other_arg=ref)
    # result = RougeScore.computa(pred, ref)
    print(result)
