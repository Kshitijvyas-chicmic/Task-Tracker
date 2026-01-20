from fastapi import FastAPI
from core.utils.database import engine, Base
import models  
from routes.user import router as user_router
from routes.role import router as role_router
from routes.task import router as task_router
from routes.comment import router as comment_router
from routes.auth import router as auth_router

app = FastAPI(title="Task Tracker")

app.include_router(user_router)
app.include_router(role_router)
app.include_router(task_router)
app.include_router(comment_router)
app.include_router(auth_router)