from fastapi import APIRouter, Depends, HTTPException
from models.rag import RAGRequest, RAGResponse
from app.services.rag_pipeline import RAGPipeline

router= APIRouter()

@router.post("/query", response_model=RAGResponse)
async def rag_query(
    request:RAGRequest,
    retriever=Depends(getvectorstore),
    llm=Depends(get_llm_client)
):
