from fastapi import APIRouter, Request, status
from sqlalchemy.orm import Session
from core.utils.database import SessionLocal
from services.activity_log_service import log_activity

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/email")
async def email_webhook(request: Request):
    payload = await request.json()

    event = payload.get("event")
    email = payload.get("email")
    task_id = payload.get("task_id")

    db: Session = SessionLocal()
    try:
        log_activity(
            db,
            actor_id=0,
            action=f"email_{event}",
            entity="task",
            entity_id=task_id,
            old_value=None,
            new_value=str(payload)
        )
        db.commit()
    finally:
        db.close()

    return {"status":"ok"}