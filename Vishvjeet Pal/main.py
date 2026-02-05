from fastapi import FastAPI
from core.utils.database import engine, Base
import models  
from routes.user import router as user_router
from routes.role import router as role_router
from routes.task import router as task_router
from routes.comment import router as comment_router
from routes.auth import router as auth_router
from routes.activity_log import router as activity_log_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Task Tracker", redirect_slashes=False)
app.dependency_overrides.clear()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development only
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