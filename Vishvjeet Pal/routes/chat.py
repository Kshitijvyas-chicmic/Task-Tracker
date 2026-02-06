# routes/chat.py
from fastapi import APIRouter, HTTPException, Query
from agent.runtime import agent
from typing import Optional

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
def chat(query: str, thread_id: Optional[str] = Query("default-session")):
    """
    Endpoint to interact with the LangGraph Task Agent.
    """
    try:
        config = {"configurable": {"thread_id": thread_id}}
        
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]}, 
            config=config
        )
        
        messages = response.get("messages", [])
        if not messages:
            return {"answer": "Agent processed the request but returned no message.", "thread_id": thread_id}
            
        return {
            "answer": messages[-1].content,
            "thread_id": thread_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")