from fastapi import FastAPI
from routes.user import router as user_router
from routes.role import router as role_router
from routes.task import router as task_router
from routes.comment import router as comment_router
from routes.auth import router as auth_router
from routes.activity_log import router as activity_log_router
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.deadline_checker import run_deadline_checker

app = FastAPI(title="Task Tracker", redirect_slashes=False)
app.dependency_overrides.clear()

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

scheduler = BackgroundScheduler()
scheduler.add_job(
    run_deadline_checker,
    trigger = "interval",
    minutes = 5,
    id = "deadline_checker",
    replace_existing = True
)

@app.on_event("startup")
def start_scheduler():
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()