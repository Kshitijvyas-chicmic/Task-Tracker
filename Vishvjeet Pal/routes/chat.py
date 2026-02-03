from fastapi import APIRouter, HTTPException
import llm.rag_state as rag_state

router=APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
def chat(query: str):
    if rag_state.rag_chain is None:
        raise HTTPException(status_code=500, detail="RAG bot not initialized")
    
    result = rag_state.rag_chain.invoke(query)
    return {"answer":result}