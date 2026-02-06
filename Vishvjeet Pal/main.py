# main.py
from fastapi import FastAPI
from routes.user import router as user_router
from routes.role import router as role_router
from routes.task import router as task_router
from routes.comment import router as comment_router
from routes.auth import router as auth_router
from routes.activity_log import router as activity_log_router
from routes.debug import router as debug_router
from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.deadline_checker import run_deadline_checker
from core.utils.config import settings
from core.utils.rate_limiter import RateLimitMiddleware, global_limiter

from core.utils.redis_checkpointer import checkpointer, _saver_context

from contextlib import asynccontextmanager
from mcp.client.stdio import stdio_client
from mcp import ClientSession
from core.utils.mcp_config import server_params
mcp_state = {"session": None, "cleanup": None}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Connect to MCP Server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_state["session"] = session
            print("Successfully connected to Task Agent MCP Server")
            yield
    # SHUTDOWN: Connection closes automatically here
    print("Disconnected from MCP Server")

app = FastAPI(title="Task Tracker", lifespan=lifespan, redirect_slashes=False)

app.add_middleware(RateLimitMiddleware, limiter=global_limiter, enabled=settings.RATE_LIMIT_ENABLED)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(task_router)
app.include_router(comment_router)
app.include_router(auth_router)
app.include_router(activity_log_router)
app.include_router(debug_router)
app.include_router(chat_router)

scheduler = BackgroundScheduler()
scheduler.add_job(run_deadline_checker, trigger="interval", minutes=5, id="deadline_checker", replace_existing=True)

@app.on_event("startup")
def startup_event():
    scheduler.start()
    try:
        checkpointer.setup()
        print("Agent Redis Checkpointer initialized.")
    except Exception as e:
        print(f"Redis Setup Error: {e}")

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    _saver_context.__exit__(None, None, None)
    print("Agent Redis connection closed.")