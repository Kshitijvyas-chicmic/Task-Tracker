from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    assigned_to: Optional[int]= None
    created_by: Optional[int]= None

class TaskAssign(BaseModel):
    user_id: int

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: str
    status: Optional[str]= None
    assigned_to: Optional[int]= None
    created_by: Optional[int]= None
    class Config:
        from_attributes = True
