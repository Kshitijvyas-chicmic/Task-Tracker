from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.utils.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    __table_args__ = {"sqlite_autoincrement": True} 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    actor_id = Column(Integer, ForeignKey("users.e_id"), nullable=False)
    action = Column(String, nullable=False)        # e.g. assign_task
    entity = Column(String, nullable=False)        # e.g. task, user
    entity_id = Column(Integer, nullable=True)     # e.g. task_id

    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
