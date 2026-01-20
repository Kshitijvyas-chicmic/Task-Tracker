from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.utils.deps import get_db
from core.utils.permissions import require_permission
from services.task_service import create_task, get_all_tasks, update_task, delete_task
from schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse
)
def add_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(require_permission("create_task"))
):
    return create_task(db, task)


@router.get(
    "/",
    response_model=list[TaskResponse]
)
def list_tasks(
    db: Session = Depends(get_db),
    user=Depends(require_permission("view_tasks"))
):
    return get_all_tasks(db)


@router.post("/approve/{task_id}")
def approve_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("approve_task"))
):
    return {"message": f"Task {task_id} approved"}

@router.put("/{task_id}")
def edit_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(require_permission("edit_task"))
):
    return update_task(db, task_id, task, user)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("delete_task"))
):
    return delete_task(db, task_id)

