from pydantic import BaseModel

class CommentCreate(BaseModel):
    task_id: int
    content: str
    e_id: int

class CommentResponse(BaseModel):
    c_id: int
    task_id: int
    e_id: int
    content: str
    timestamp: str

    class Config:
        from_attributes = True