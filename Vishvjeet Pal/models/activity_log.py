from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.utils.database import Base
from datetime import datetime

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    __table_args__ = {"sqlite_autoincrement": True} 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    actor_id = Column(Integer, ForeignKey("users.e_id"), nullable=False)
    action = Column(String, nullable=False)        
    entity = Column(String, nullable=False)        
    entity_id = Column(Integer, nullable=True)     

    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)

    timestamp = Column(DateTime, default=datetime.now)
