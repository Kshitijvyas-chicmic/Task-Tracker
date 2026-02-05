from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.utils.database import Base

class User(Base):
    __tablename__="users"

    e_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    r_id = Column(Integer, ForeignKey('roles.r_id'))
    team = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True)
    password= Column(String)

    role = relationship("Role", back_populates="users")