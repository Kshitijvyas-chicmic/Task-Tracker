from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from schemas.role import RoleCreate, RoleResponse
from services.role_service import create_role, get_all_roles, delete_role_service, update_role_service
from core.utils.permissions import require_permission

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleResponse)
def add_role(role: RoleCreate, db: Session = Depends(get_db), current_user= Depends(require_permission("create_role"))):
    return create_role(db, role, current_user["sub"])

@router.get("/", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db), current_user= Depends(require_permission("view_role"))):
    return get_all_roles(db, current_user["sub"])

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user= Depends(require_permission("delete_role"))):
    return delete_role_service(db, role_id, current_user["sub"])

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_data: RoleCreate, db: Session = Depends(get_db), current_user= Depends(require_permission("update_role"))):
    return update_role_service(db, role_id, role_data, current_user["sub"])