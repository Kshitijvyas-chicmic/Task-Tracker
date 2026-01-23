from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.utils.deps import get_db, get_current_user
from schemas.user import UserCreate, UserResponse
from services.user_service import create_user, get_all_users, update_user, delete_user
from core.utils.permissions import require_permission
from core.utils.pagination import pagination_params
from services.user_service import add_role_to_user

router=APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db), current_user=Depends(require_permission("create_user"))):
    return create_user(db, user, current_user['sub'])

@router.get("/")
def list_users(pagination=Depends(pagination_params),current_user=Depends(require_permission("view_users")), db: Session = Depends(get_db)):
    total, users = get_all_users(db, current_user['sub'], pagination["offset"], pagination["size"])
    return {
        "page": pagination["page"],
        "size": pagination["size"],
        "total": total,
        "data": users
    }

@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("update_user"))
):
    return update_user(db, user_id, user, current_user)

@router.delete("/{user_id}")
def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("delete_user"))
):
    return delete_user(db, user_id, current_user['sub'])

@router.put("/{user_id}/role")
def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("manage_roles"))
):
    return add_role_to_user(user_id, role_id, db, user['sub'])