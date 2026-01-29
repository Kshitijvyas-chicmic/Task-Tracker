from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.utils.database import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pending")
    priority = Column(String, default="medium")
    deadline = Column(Date, nullable=True)
    assigned_to  = Column(Integer, ForeignKey("users.e_id"), nullable=True)
    created_by= Column(Integer, ForeignKey("users.e_id"))
    last_escalated_level = Column(Integer, default=0, nullable=False)
    
    assignee = relationship("User", foreign_keys=[assigned_to])
    creator = relationship("User", foreign_keys=[created_by])
