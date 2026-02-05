from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.activity_log import ActivityLog

def log_activity(
    db: Session,
    actor_id: int,
    action: str,
    entity: str,
    entity_id: int | None = None,
    old_value: str | None = None,
    new_value: str | None = None
):
    log = ActivityLog(
        actor_id=actor_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        old_value=old_value,
        new_value=new_value
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_activity_logs(db, offset: int, limit: int):
    query = db.query(ActivityLog).order_by(ActivityLog.timestamp.desc())
    total = query.count()
    data = query.offset(offset).limit(limit).all()

    return total, data

def get_activity_by_id(db: Session, user_id: int, offset: int, limit: int):
    query = db.query(ActivityLog).filter(ActivityLog.actor_id == user_id)
    total = query.count()
    logs = query.offset(offset).limit(limit).all()
    if not logs:
        raise HTTPException(status_code=404, detail="Log not found")
    
    return total, logs