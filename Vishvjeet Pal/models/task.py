from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.utils.database import Base

class Task(Base):
    __tablename__="tasks"

    task_id=Column(Integer, primary_key=True, index=True)
    title=Column(String, index=True)
    e_id=Column(Integer, ForeignKey('users.e_id'))
    timestamp=Column(DateTime, default=func.now())
    status=Column(String)
    deadline=Column(DateTime)

    user = relationship("User")