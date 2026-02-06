# # routes/chat.py
# from fastapi import APIRouter, HTTPException, Query
# from agent.runtime import agent
# from typing import Optional

# router = APIRouter(prefix="/chat", tags=["Chat"])

# @router.post("/")
# def chat(query: str, thread_id: Optional[str] = Query("default-session")):
#     """
#     Endpoint to interact with the LangGraph Task Agent.
#     """
#     try:
#         config = {"configurable": {"thread_id": thread_id}}
        
#         response = agent.invoke(
#             {"messages": [{"role": "user", "content": query}]}, 
#             config=config
#         )
        
#         messages = response.get("messages", [])
#         if not messages:
#             return {"answer": "Agent processed the request but returned no message.", "thread_id": thread_id}
            
#         return {
#             "answer": messages[-1].content,
#             "thread_id": thread_id
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

from fastapi import APIRouter, HTTPException
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

router = APIRouter(prefix="/chat", tags=["Chat"])

server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"], # Your MCP server file path
)

@router.post("/")
async def chat(query: str, thread_id: str = "default-session"):
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                result = await session.call_tool(
                    "agent_execute", 
                    arguments={
                        "prompt": query,
                        "thread_id": thread_id
                    }
                )
                
                answer = result.content[0].text if result.content else "No response."
                return {"answer": answer, "thread_id": thread_id}
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MCP Error: {str(e)}")