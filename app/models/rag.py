from pydantic import BaseModel, Field
from typing import List
from models.metrics import MetricResult


class RAGRequest(BaseModel):
    query: str = Field(description="query for the rag system")
    k: int = Field(description="", default=3)

class Document(BaseModel):
    id: str
    text: str
    source: str

class RAGResponse(BaseModel):
    summary: str
    retrieved_docs: List[Document]

class SummaryRequest(BaseModel):
    text: str
    abstract: str
    paper_id: int

class SummaryResponse(BaseModel):
    summary: str
    paper_id: int

class EvaluationRequest(BaseModel):
    generated_text: str
    reference_text: str
    paper_id: int

class EvaluationResponse(BaseModel):
    metrics: List[MetricResult]
