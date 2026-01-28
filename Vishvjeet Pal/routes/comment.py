from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from core.utils.permissions import require_permission
from services.comment_service import add_comment, get_comments_by_task, delete_comment
from schemas.comment import CommentCreate, CommentResponse


router=APIRouter(prefix="/comments", tags=["comments"])

@router.post("/task/{task_id}", response_model=CommentResponse)
def create_comment(task_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("add_task_comment"))):
    return add_comment(db, task_id, comment, current_user["sub"])

@router.get("/task/{task_id}", response_model=list[CommentResponse])
def read_comments_by_task(task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("view_comments"))):
    return get_comments_by_task(db, task_id, current_user["sub"])

@router.delete("/{c_id}")
def delete_comment_by_id(c_id, db = Depends(get_db), current_user = Depends(require_permission("delete_comment"))):
    return delete_comment(db, c_id, current_user["sub"])