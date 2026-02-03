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

# Rate limiter
from core.utils.config import settings
from core.utils.rate_limiter import RateLimitMiddleware, global_limiter

# RAG based llm
from llm.rag_bot import load_rag_bot
import llm.rag_state as rag_state

app = FastAPI(title="Task Tracker", redirect_slashes=False)
app.dependency_overrides.clear()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware, limiter=global_limiter, enabled=settings.RATE_LIMIT_ENABLED)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(task_router)
app.include_router(comment_router)
app.include_router(auth_router)
app.include_router(activity_log_router)
app.include_router(debug_router)
app.include_router(chat_router)
scheduler = BackgroundScheduler()
scheduler.add_job(
    run_deadline_checker,
    trigger = "interval",
    minutes = 5,
    id = "deadline_checker",
    replace_existing = True
)

@app.on_event("startup")
def startup_event():
    scheduler.start()

    rag_state.rag_chain, rag_state.retriever = load_rag_bot()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()