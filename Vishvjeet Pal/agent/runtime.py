from langchain.agents import create_agent
# from langchain.agents.middleware import HumanInTheLoopMiddleware
# from langgraph.checkpoint.memory import InMemorySaver
from core.utils.redis_checkpointer import checkpointer
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from agent.tools import list_tasks, create_task, delete_task, add_comment, list_comments, list_users, create_user, delete_user, update_user, list_roles, delete_comment
import os
from core.utils.config import settings

# memory = InMemorySaver()

# 1. Define tools
tools = [list_tasks, create_task, delete_task, add_comment, list_comments, list_users, create_user, delete_user, update_user, list_roles, delete_comment]

# 2. Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    api_key=settings.GROQ_API_KEY,   
    temperature=0.2
)

# 3. Assemble the Agent
agent = create_agent(
    llm, 
    checkpointer=checkpointer,
    tools=tools,
    # checkpointer=memory,
    # middleware=[
    #     HumanInTheLoopMiddleware(
    #         interrupt_on={
    #             "delete_task": True,
    #             "create_task": True,
    #             "add_comment": False,
    #             "list_tasks": False,
    #             "list_users": False 
    #         },
    #         description_prefix="Action pending your approval"
    #     )
    # ],
    system_prompt = """
You are a Task Management Assistant. 
CORE RULE: When a tool returns information (like a list of tasks), your ONLY job is to report that information to the user.

1. You have access to tools that connect to a database. 
2. If the tool returns a list of tasks, say "Here are your tasks:" and list them.
3. NEVER claim you cannot access external systems. The tools provide that access for you.
4. If a tool returns data, use that data to answer. Do not apologize or refuse.
5. Give answer from the response you get ONLY from tools. NEVER make up answer.
STRICT LIMITATIONS:
1. ONLY execute the specific command given by the user in the prompt.
2. DO NOT call any tools that were not explicitly requested (e.g., if asked to list users, do NOT delete tasks).
3. STOP IMMEDIATELY after calling the requested tool and reporting the result.
4. NEVER perform destructive actions (delete) unless the word 'delete' is in the user's prompt.
"""
)
