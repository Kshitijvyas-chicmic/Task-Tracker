from datetime import datetime 
from sqlalchemy.orm import Session 
from core.utils.database import SessionLocal
from core.utils.email import send_email
from models.task import Task
from models.user import User
from services.escalation_service import get_active_escalation_rules
from services.activity_log_service import log_activity

SYSTEM_ACTOR_ID = 0

def run_deadline_checker():
    db: Session = SessionLocal()
    try:
        _process_overdue_tasks(db)
    finally:
        db.close()

def _process_overdue_tasks(db: Session):
    now = datetime.utcnow()

    overdue_tasks = (
        db.query(Task)
        .filter(
            Task.deadline.isnot(None),
            Task.deadline < now,
            Task.status != "completed"
        )
        .all()
    )

    if not overdue_tasks:
        return
    
    rules = get_active_escalation_rules(db)

    for task in overdue_tasks:
        _apply_escalation(task, rules, db)

def _apply_escalation(task: Task, rules, db: Session):
    now = datetime.utcnow()

    minutes_overdue = int((now - task.deadline).total_seconds() / 60)

    for rule in rules:
        if rule.level <= task.last_escalated_level:
            continue

        if minutes_overdue >= rule.after_minutes:
            old_state = {
                "last_escalated_level": task.last_escalated_level,
                "priority": task.priority,
                "assigned_to": task.assigned_to 
            }

            _execute_action(task, rule, db)

            task.last_escalated_level = rule.level
            db.commit()
            db.refresh(task)

            new_state = {
                "last_escalated_level": task.last_escalated_level,
                "priority": task.priority,
                "assigned_to": task.assigned_to,
                "action": rule.action
            }

            log_activity(
                db,
                actor_id = SYSTEM_ACTOR_ID,
                action = "escalate_task",
                entity = "task",
                entity_id = task.task_id,
                old_value = str(old_state),
                new_value = str(new_state)
            )

            break 

def _execute_action(task: Task, rule, db: Session):
    if rule.action == "priority_up":
        if task.priority == "low":
            task.priority = "medium"
        elif task.priority == "medium":
            task.priority = "high"

    elif rule.action == "reassign":
        task.assigned_to = task.created_by

    elif rule.action == "email":
        name,email = _resolve_email(task, rule.notify_role, db)

        if email:
            send_email(
                to_email=email,
                subject = f"Task Escalated: {task.title}",
                content=(
                    f"Hello {name}\n\n"
                    f"Task '{task.title}' is overdue.\n\n"
                    f"Deadline: {task.deadline}\n"
                    f"Current Priority: {task.priority}\n"
                    f"Escalation Level: {rule.level}\n"
                )
            )
        # print(f"[ESCALATION EMAIL] Task {task.task_id} -> {rule.notify_role}")

def _resolve_email(task, notify_role, db):
    if notify_role == "assignee" and task.assigned_to:
        user = db.query(User).filter(User.e_id == task.assigned_to).first()
        return (user.name,user.email) if user else None 
    
    if notify_role == "manager":
        manager = db.query(User).filter(User.r_id == 2).first()
        return (manager.name,manager.email) if manager else None 
    
    if notify_role == "admin":
        admin = db.query(User).filter(User.r_id == 1).first()
        return (admin.name,admin.email) if admin else None
    return None