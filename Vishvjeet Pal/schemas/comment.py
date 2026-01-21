from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    task_id: int
    content: str
    e_id: int

class CommentResponse(BaseModel):
    c_id: int
    task_id: int
    e_id: int
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True