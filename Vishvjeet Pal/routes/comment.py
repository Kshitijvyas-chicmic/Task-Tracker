from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from services.comment_service import add_comment, get_comments_by_task
from schemas.comment import CommentCreate, CommentResponse

router=APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return add_comment(db, comment)

@router.get("/task/{task_id}", response_model=list[CommentResponse])
def read_comments_by_task(task_id: int, db: Session = Depends(get_db)):
    return get_comments_by_task(db, task_id)