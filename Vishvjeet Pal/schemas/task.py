from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    e_id: int
    status: str
    deadline: Optional[str]  

class TaskResponse(BaseModel):
    task_id: int
    title: str
    e_id: int
    status: str
    deadline: Optional[str]
    timestamp: str