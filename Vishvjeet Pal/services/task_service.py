from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreate
from fastapi import HTTPException, status
def create_task(db: Session, task_data: TaskCreate):
    task=Task(**task_data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_all_tasks(db: Session):
    return db.query(Task).all()

def update_task(db, task_id: int, task_data, user: dict):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    user_id = int(user["sub"])
    permissions = user.get("permissions", [])

    if "edit_task" in permissions:
        pass
    else:
        if task.assignee_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your assigned tasks"
            )

    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

def delete_task(db, task_id: int, user: dict):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    permissions = user.get("permissions", [])

    if "delete_task" not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete tasks"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}