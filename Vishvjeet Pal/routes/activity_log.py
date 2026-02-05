from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils.deps import get_db
from core.utils.permissions import require_permission
from core.utils.pagination import pagination_params
from services.activity_log_service import get_activity_logs

router = APIRouter(prefix="/activity-logs", tags=["Audit Logs"])

@router.get("/")
def list_activity_logs(
    pagination=Depends(pagination_params),
    db: Session = Depends(get_db),
    user=Depends(require_permission("view_audit_logs"))
):
    total, logs = get_activity_logs(
        db,
        pagination["offset"],
        pagination["size"]
    )

    return {
        "page": pagination["page"],
        "size": pagination["size"],
        "total": total,
        "data": logs
    }
