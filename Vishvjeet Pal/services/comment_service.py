from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate

def add_comment(db: Session, comment_data: CommentCreate):
    comment = Comment(**comment_data.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments_by_task(db: Session, task_id: int):
    return db.query(Comment).filter(Comment.task_id == task_id).all()