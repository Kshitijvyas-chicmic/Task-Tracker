from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    task_id: Optional[int] = None
    content: str
    e_id: Optional[int] = None

class CommentResponse(BaseModel):
    c_id: int
    task_id: int
    e_id: int
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True