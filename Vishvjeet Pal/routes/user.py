from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.utils.deps import get_db, get_current_user
from schemas.user import UserCreate, UserResponse
from services.user_service import create_user, get_all_users, update_user, delete_user
from core.utils.security import get_current_user
from core.utils.permissions import require_admin, require_permission

router=APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=list[UserResponse])
def list_users(current_user=Depends(require_permission("view_users")),db: Session = Depends(get_db)):
    return get_all_users(db)

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
    return delete_user(db, user_id)
