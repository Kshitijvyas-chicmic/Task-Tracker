from fastmcp import FastMCP
from agent.runtime import agent, llm
from langgraph.types import Command
import asyncio
import uuid
from typing import Optional
from core.utils.redis_checkpointer import checkpointer

# 1. Initialize FastMCP with instructions
mcp = FastMCP(
    name="task-tracker-agent",
    instructions="""
    YOU ARE AN AUTONOMOUS EXECUTION ENGINE.
    You can create, delete, and comment on tasks in a task tracking system.
    """
)

redis_ready = False

async def initialize_redis():
    """Manually initializes Redis since on_start is unavailable."""
    global redis_ready
    if not redis_ready:
        checkpointer.setup() 
        redis_ready = True
        # print("redis Checkpointer initialized.")

@mcp.tool
async def agent_execute(prompt: str, thread_id: Optional[str] = None) -> str:
    """Executes a task with persistent Redis memory."""
    await initialize_redis() # Ensure Redis is ready before execution
    
    try:
        t_id = thread_id if thread_id else str(uuid.uuid4())
        config = {"configurable": {"thread_id": t_id}}
        
        response = agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}, 
            config=config
        )
        
        messages = response.get("messages", [])
        return str(messages[-1].content) if messages else "No response generated."
    except Exception as e:
        print(e)
        return f"Error: {e}"
active_sessions={}


@mcp.tool
async def agent_respond(thread_id: str, decision: str, feedback: str = None) -> str:
    """
    Responds to a pending action request.
    Args:
        thread_id: The ID provided in the approval request.
        decision: 'approve', 'reject', or 'edit'.
        feedback: Reason for rejection or instructions for the edit.
    """
    try:
        config={"configurable":{"thread_id":thread_id}}

        if decision == "approve":
            cmd = Command(resume={"decisions": [{"type":"approve"}]})
        elif decision == "reject":
            cmd = Command(resume={"decisions": [{"type":"reject","message":feedback}]})
        else:
            return "Invalid decision type. Use 'approve' or 'reject'."
        response = await agent.ainvoke(cmd, config=config)

        if "__interrupt__" in response:
            return f"Action processed, but another interrupt was triggered: {response['__interrupt__'][0].value['action_requests'][0]['name']}"
        return response["messages"][-1].content
    except Exception as e:
        return f"Error resuming agent: {str(e)}"
    
@mcp.tool
async def ping() -> str:
    """Simple test to see if the server is alive."""
    return "pong"

@mcp.tool
async def llm_execute(prompt: str) -> str:
    """
    Direct LLM test to bypass complex agent logic.
    """
    try:
        from langchain_core.messages import HumanMessage
        # We call the LLM directly, bypassing the 'agent' wrapper
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"LLM Error: {str(e)}"

# 3. Export for ASGI
app = mcp.http_app()

if __name__ == "__main__":
    mcp.run()
