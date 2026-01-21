from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from models.role import Role
from models.permission import Permission
from core.utils.deps import get_db

MANAGER_PERMISSIONS = [
    "view_users", "create_task", "edit_task", "delete_task", "view_task",
    "assign_task", "view_audit_logs", "reassign_task", "update_task_status",
    "set_task_priority", "set_task_deadline", "add_task_comment",
    "attach_task_file", "mention_team_member", "create_project",
    "update_project", "archive_project", "assign_task_project",
    "add_team_member", "remove_team_member", "assign_role_team",
    "view_team_workload", "generate_reports", "view_dashboard",
    "receive_notifications", "approve_task", "create_recurring_task",
    "schedule_task", "export_data", "share_project_summary",
    "view_all_team_activities"
]

EMPLOYEE_PERMISSIONS = [
    "view_task", "update_task_status", "add_task_comment", "view_audit_logs", "attach_task_file",
    "mention_team_member", "view_dashboard", "receive_notifications",
]

ADMIN_PERMISSIONS = MANAGER_PERMISSIONS + EMPLOYEE_PERMISSIONS  # Full access

def get_or_create_role(db: Session, name: str) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if not role:
        role = Role(name=name)
        db.add(role)
        db.commit()
        db.refresh(role)
        print(f"Role '{name}' created")
    return role

def get_or_create_permission(db: Session, name: str) -> Permission:
    perm = db.query(Permission).filter(Permission.name == name).first()
    if not perm:
        perm = Permission(name=name)
        db.add(perm)
        db.commit()
        db.refresh(perm)
        print(f"Permission '{name}' created")
    return perm

def assign_permissions(db: Session, role: Role, permissions: list[str]):
    for perm_name in permissions:
        perm = get_or_create_permission(db, perm_name)
        if perm not in role.permissions:
            role.permissions.append(perm)
    db.commit()
    print(f"Permissions assigned to role '{role.name}'")

def seed_permissions(db: Session):
    manager_role = get_or_create_role(db, "manager")
    employee_role = get_or_create_role(db, "employee")
    admin_role = get_or_create_role(db, "admin")

    assign_permissions(db, manager_role, MANAGER_PERMISSIONS)
    assign_permissions(db, employee_role, EMPLOYEE_PERMISSIONS)
    assign_permissions(db, admin_role, ADMIN_PERMISSIONS)

    print("✅ Manager, Employee, and Admin permissions seeded successfully!")

if __name__ == "__main__":
    db = next(get_db())
    seed_permissions(db)
