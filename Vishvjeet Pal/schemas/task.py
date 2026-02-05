from pydantic import BaseModel
from typing import Optional
from datetime import date as Date

class TaskCreate(BaseModel):
    title: str
    description: str
    status: Optional[str]= "pending"
    priority: Optional[str]= "medium"
    deadline: Optional[Date]= None
    assigned_to: Optional[int]= None
    created_by: Optional[int]= None

class TaskAssign(BaseModel):
    user_id: int

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: str
    status: Optional[str]= "pending"
    priority: Optional[str]= "medium"
    deadline: Optional[Date]= None
    assigned_to: Optional[int]= None
    created_by: Optional[int]= None
    class Config:
        from_attributes = True
