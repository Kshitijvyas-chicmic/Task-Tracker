from sqlalchemy.orm import Session
from models.permission import Permission
from models.role import Role
from schemas.role import RoleCreate, RoleResponse

def create_role(db: Session, role_data: RoleCreate):
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
    return RoleResponse(
        r_id=role.r_id,  
        role=role.name,
        permissions=[permission.name for permission in role.permissions]  # Assuming 'name' is the field in Permission
    )

def get_all_roles(db: Session):
    roles= db.query(Role).all()

    return [
        RoleResponse(
            r_id=role.r_id,  # Assuming 'id' is the primary key for Role
            role=role.name,  # Assuming 'name' is the field for the role name
            permissions=[permission.name for permission in role.permissions]
        )
        for role in roles
    ]
