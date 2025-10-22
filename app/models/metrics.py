from pydantic import BaseModel, Field
from typing import Optional, Union, List
from abc import ABC, abstractmethod
import evaluate

rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")

class MetricResult(BaseModel):
    name: str
    score: float

class MetricEvaluator(ABC):
    @abstractmethod
    def compute(self, reference: str, prediction: str) -> MetricResult:
        pass

class RougeScore(MetricEvaluator):
    def compute(self, reference: str, prediction: str) -> MetricResult:
        score = rouge.compute(predictions=[prediction], references=[reference])
        return MetricResult(name='ROUGE-L', score=score)

class BertScore(MetricEvaluator):
    def compute(self, reference: str, prediction: str) -> MetricResult:
        score = bertscore.compute(predictions=[prediction], references=[reference], lang="en")
        return MetricResult(name='BERTSCORE', score=score)
