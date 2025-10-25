from fastapi import APIRouter, Depends, HTTPException
from models.rag import RAGRequest, RAGResponse, SummaryResponse, SummaryRequest
from models.rag import  EvaluationRequest, EvaluationResponse
from services.rag_pipeline import RAGPipeline, SummaryPipeline, EvaluationPipeline
from services.llm_client import get_llm_client
from db.vectorstore import get_vectorstore
from langchain_core.documents import Document

router= APIRouter()

@router.post("/query", response_model=RAGResponse)
async def rag_query(
    request:RAGRequest,
    retriever=Depends(get_vectorstore),
    llm=Depends(get_llm_client)
):
    pipeline = RAGPipeline(retriever=retriever, llm=llm)
    result = await pipeline.run(query=request.query, top_k=request.k)

    # Ensure the response matches RAGResponse schema
    docs = [Document(**d) for d in result["retrieved_docs"]]
    return RAGResponse(summary=result["summary"], retrieved_docs=docs)

@router.post("/summary", response_model=SummaryResponse)
async def summary_request(
    request:SummaryRequest,
    llm=Depends(get_llm_client)
):
    pipeline = SummaryPipeline(llm=llm)
    result = await pipeline.run(text=request.text)
    return SummaryResponse(summary=result["summary"], paper_id=request.paper_id)

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluation_request(
    request:EvaluationRequest
):
    pipeline = EvaluationPipeline()
    print(request.reference_text)
    print(request.generated_text)
    results = await pipeline.run(
        generated_text=request.generated_text,
        reference_text=request.reference_text
    )
    return EvaluationResponse(metrics=results)