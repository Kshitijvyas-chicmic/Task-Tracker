from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from core.utils.permissions import require_permission
from models.permission import Permission

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.get("/")
def list_permissions(
    db: Session = Depends(get_db),
    user=Depends(require_permission("manage_roles"))
):
    return [{"id": p.id, "name": p.name} for p in db.query(Permission).all()]
