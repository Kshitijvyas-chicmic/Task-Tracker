from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from schemas.role import RoleCreate, RoleResponse
from services.role_service import create_role, get_all_roles

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleResponse)
def add_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)

@router.get("/", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return get_all_roles(db)
