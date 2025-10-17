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
    pipeline = RAGPipeline(retriever=retriever, llm=llm)
    result = await pipeline.run(query=request.query, k=request.k)

    # Ensure the response matches RAGResponse schema
    docs = [Document(**d) for d in result["retrieved_docs"]]
    return RAGResponse(summary=result["summary"], retrieved_docs=docs)
