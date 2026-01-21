from logging import log
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