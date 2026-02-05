from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from core.utils.database import Base
from .permission import Permission

# Association table for Role <-> Permission
role_permissions = Table(
    "role_permissions", Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.r_id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"

    r_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role")
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )
