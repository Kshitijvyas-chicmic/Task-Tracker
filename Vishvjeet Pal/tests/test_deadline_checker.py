from datetime import datetime, timedelta
from unittest.mock import patch

from models.task import Task
from models.user import User
from models.escalation_rule import EscalationRule

from core.utils.database import SessionLocal
from jobs.deadline_checker import run_deadline_checker

def test_email_escalation_for_overdue_task(db_session):
    creator = User(e_id=1, name = "Manager", email= "manager@test.com", r_id = 2)
    assignee = User(e_id = 2, name= "Dev", email = "dev@test.com", r_id = 3)

    db_session.add_all([creator, assignee])
    db_session.commit()

    rule = EscalationRule(
        level = 1,
        after_minutes = 10,
        action = "email",
        notify_role = "manager",
        is_active = True 
    )

    db_session.add(rule)
    db_session.commit()

    task = Task(
        title = "Overdue Task",
        description = "Test escalation",
        status = "pending",
        priority = "low",
        deadline = datetime.utcnow() - timedelta(minutes = 30),
        created_by = creator.e_id,
        assigned_to = assignee.e_id,
        last_escalated_level = 0
    )

    db_session.add(task)
    db_session.commit()

    with patch("jobs.deadline_checker.SessionLocal", return_value= db_session),patch("jobs.deadline_checker.log_activity"),patch("services.activity_log_service.log_activity"), patch("jobs.deadline_checker.send_email") as mock_email:
        run_deadline_checker()

        updated_task = db_session.query(Task).first()
        assert updated_task.last_escalated_level == 1

        mock_email.assert_called_once()

def test_skip_already_escalated_level(db_session):
    user = User(e_id=1, name="Manager", email = "manager@test.com", r_id=2)
    db_session.add(user)
    db_session.commit()

    rule = EscalationRule(
        level = 1,
        after_minutes = 5, 
        action = "priority_up",
        is_active = True 
    )

    db_session.add(rule)
    db_session.commit()

    task = Task(
        title = "Already escalated",
        description = "Should be skipped",
        status = "pending",
        priority = "medium",
        deadline = datetime.utcnow() - timedelta(minutes=20),
        created_by = 1,
        last_escalated_level = 1
    )

    db_session.add(task)
    db_session.commit()

    with patch("jobs.deadline_checker.SessionLocal", return_value= db_session), patch("jobs.deadline_checker.log_activity"),patch("services.activity_log_service.log_activity"):
        run_deadline_checker()

        updated_task = db_session.query(Task).first()
        assert updated_task.priority == "medium"
    
def test_priority_up_escalation(db_session):
    user = User(e_id=1, name="Manager", email="manager@test.com", r_id=2)
    db_session.add(user)
    db_session.commit()

    rule = EscalationRule(
        level=1,
        after_minutes=5,
        action='priority_up',
        is_active=True 
    )
    db_session.add(rule)
    db_session.commit()

    task = Task(
        title="Priority Task",
        description="priority should be raised",
        status="pending",
        priority="low",
        deadline=datetime.utcnow() - timedelta(minutes=10),
        created_by=1,
        last_escalated_level=0
    )
    db_session.add(task)
    db_session.commit()

    with patch("jobs.deadline_checker.SessionLocal", return_value= db_session), patch("jobs.deadline_checker.log_activity"),patch("services.activity_log_service.log_activity"):
        run_deadline_checker()

        updated_task = db_session.query(Task).first()
        assert updated_task.priority == "medium"
        assert updated_task.last_escalated_level == 1

def test_no_overdue_tasks(db_session):
    task = Task(
        title="future task",
        description="No escalation",
        status="pending",
        deadline=datetime.utcnow()+timedelta(minutes=30),
        created_by=1,
        last_escalated_level=0
    )
    db_session.add(task)
    db_session.commit()

    with patch("jobs.deadline_checker.SessionLocal", return_value= db_session), patch("jobs.deadline_checker.send_email") as mock_email:
        run_deadline_checker()

        mock_email.assert_not_called()