from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.permission import Permission
from models.role import Role
from schemas.role import RoleCreate, RoleResponse
from services.activity_log_service import log_activity


def create_role(db: Session, role_data: RoleCreate, actor_id: int) -> RoleResponse:
    role = Role(name=role_data.role)

    permissions = (
        db.query(Permission)
        .filter(Permission.name.in_(role_data.permissions))
        .all()
    )

    role.permissions.extend(permissions)

    db.add(role)
    db.commit()
    db.refresh(role)

    log_activity(
        db=db,
        actor_id=actor_id,
        action="create_role",
        entity="role",
        entity_id=role.r_id
    )

    return RoleResponse(
        r_id=role.r_id,  
        role=role.name,
        permissions=[permission.name for permission in role.permissions]  
    )

def get_all_roles(db: Session, actor_id: int) -> list[RoleResponse]:
    roles= db.query(Role).all()

    log_activity(
        db=db,
        actor_id=actor_id,
        action="view_role",
        entity="role",
        entity_id=None,
    )

    return [
        RoleResponse(
            r_id=role.r_id,  
            role=role.name,  
            permissions=[permission.name for permission in role.permissions]
        )
        for role in roles
    ]

def delete_role_service(db: Session, role_id: int, actor_id: int):
    role = db.query(Role).filter(Role.r_id==role_id).first()
    if role:
        db.delete(role)
        db.commit()
        log_activity(
            db=db,
            actor_id=actor_id,
            action="delete_role",
            entity="role",
            entity_id=role.r_id
        )
        return {"message": "Role deleted successfully"}
    return {"message": "Role not found"}

def update_role_service(db: Session, role_id: int, role_data: RoleCreate, actor_id: int) -> RoleResponse:
    role=db.query(Role).filter(Role.r_id==role_id).first()
    if not role:
        raise HTTPException(404, "Role not found")
    old_value = role.name    
    role.name = role_data.role
    permissions = (
        db.query(Permission)
        .filter(Permission.name.in_(role_data.permissions))
        .all()
    )
    role.permissions = permissions

    log_activity(
        db=db,
        actor_id=actor_id,
        action="update_role",   
        entity="role",
        entity_id=role.r_id,
        old_value=  old_value,
        new_value= role_data.role
    )
    db.commit()
    db.refresh(role)
    return RoleResponse(
        r_id=role.r_id,  
        role=role.name,
        permissions=[permission.name for permission in role.permissions]
    )