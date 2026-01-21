from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from core.utils.permissions import require_permission
from services.comment_service import add_comment, get_comments_by_task
from schemas.comment import CommentCreate, CommentResponse

router=APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("add_task_comment"))):
    return add_comment(db, comment, current_user["sub"])

@router.get("/task/{task_id}", response_model=list[CommentResponse])
def read_comments_by_task(task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("view_comments"))):
    return get_comments_by_task(db, task_id, current_user["sub"])