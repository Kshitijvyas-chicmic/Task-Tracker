from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.task_service import get_task_by_id
from core.utils.deps import get_db
from core.utils.permissions import require_permission
from core.utils.pagination import pagination_params
from services.task_service import assign_task, create_task, get_all_tasks, update_task, delete_task_service
from schemas.task import TaskAssign, TaskCreate, TaskResponse

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
    return create_task(db, task, user["sub"])


@router.get(
    "/",
    response_model=list[TaskResponse]
)
def list_tasks(
    pagination=Depends(pagination_params),
    db: Session = Depends(get_db),
    user=Depends(require_permission("view_task"))
):
    total, tasks = get_all_tasks(db, user["sub"], pagination["offset"], pagination["size"])
    return {
        "page": pagination["page"],
        "size": pagination["size"],
        "total": total,
        "data": tasks
    }

@router.post("/approve/{task_id}")
def approve_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("approve_task"))
):
    return {"message": f"Task {task_id} approved"}

@router.put("/edit/{task_id}")
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
    return delete_task_service(db, task_id, user)

@router.put("/{task_id}/assign", response_model=TaskResponse)
def assign_task_to_user(
    task_id: int,
    payload: TaskAssign,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("assign_task"))
):
    return assign_task(
        db,
        task_id,
        payload.user_id,
        actor_id=current_user["sub"]
    )

@router.get("/{user_id}")
def get_task(user_id: int, pagination=Depends(pagination_params), db: Session = Depends(get_db), current_user=Depends(require_permission('view_task'))):
    total, tasks = get_task_by_id(db, user_id, current_user["sub"], pagination["offset"], pagination["size"])
    return {
        "page": pagination["page"],
        "size": pagination["size"],
        "total": total,
        "data": tasks
    }