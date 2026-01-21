from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate
from services.activity_log_service import log_activity

def add_comment(db: Session, comment_data: CommentCreate, actor_id: int):
    comment = Comment(**comment_data.model_dump())
    db.add(comment)
    db.commit()
    log_activity(
        db,
        actor_id=actor_id,
        action=f"Added comment to task {comment_data.task_id}",
        entity="comment",
        entity_id=comment.id
    )
    db.refresh(comment)
    return comment

def get_comments_by_task(db: Session, task_id: int, actor_id: int):

    log_activity(
        db,
        actor_id=actor_id,
        action=f"Viewed comments for task {task_id}",
        entity="comment"
    )
    
    return db.query(Comment).filter(Comment.task_id == task_id).all()
    return db.query(Comment).filter(Comment.task_id == task_id).all()