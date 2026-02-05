from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreate, TaskResponse
from fastapi import HTTPException, status
from models.user import User
from services.activity_log_service import log_activity

def create_task(db: Session, task_data: TaskCreate) -> TaskResponse:
    task = Task(**task_data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskResponse(task_id=task.task_id, title=task.title, description=task.description)

def get_all_tasks(db: Session):
    tasks= db.query(Task).all()
    return [TaskResponse(task_id=task.task_id, title=task.title, description=task.description) for task in tasks]

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

def delete_task_service(db, task_id: int, user: dict):
    task = db.query(Task).filter(Task.task_id == task_id).first()

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

def assign_task(db, task_id: int, user_id: int, actor_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    user = db.query(User).filter(User.e_id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    old_assignee = task.assigned_to
    task.assigned_to = user_id

    db.commit()
    db.refresh(task)

    log_activity(
        db=db,
        actor_id=actor_id,
        action="assign_task",
        entity="task",
        entity_id=task_id,
        old_value=str(old_assignee),
        new_value=str(user_id)
    )
    return task

