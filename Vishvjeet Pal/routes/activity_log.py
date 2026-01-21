from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from core.utils.permissions import require_permission
from models.activity_log import ActivityLog

router = APIRouter(prefix="/activity-logs", tags=["Audit Logs"])

@router.get("/")
def get_logs(
    db: Session = Depends(get_db),
    user=Depends(require_permission("view_audit_logs"))
):
    return db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).all()
