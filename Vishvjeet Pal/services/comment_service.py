from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate
from services.activity_log_service import log_activity

def add_comment(db: Session, task_id: int, comment_data: CommentCreate, actor_id: int):
    comment = Comment(**comment_data.model_dump())
    comment.e_id=actor_id
    comment.task_id=task_id
    db.add(comment)
    db.commit()
    log_activity(
        db,
        actor_id=actor_id,
        action=f"Added comment to task {comment.task_id}",
        entity="comment",
        entity_id=comment.c_id
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
def delete_comment(db: Session, c_id: int, actor_id):
    comment = db.query(Comment).filter(Comment.c_id==c_id).first()
    if comment:
        db.delete(comment)
        db.commit()

        log_activity(
            db,
            actor_id=actor_id,
            action="Comment deleted",
            entity="Comment",
            entity_id=c_id
        )
        return {"message":"Comment deleted successfully"}
    return {"message":"No comment found"}
