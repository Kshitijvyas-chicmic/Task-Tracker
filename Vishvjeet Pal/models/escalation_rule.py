from sqlalchemy import Column, Integer, String, Boolean
from core.utils.database import Base

class EscalationRule(Base):
    __tablename__ = "escalation_rules"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)
    after_minutes = Column(Integer, nullable=False)

    action = Column(String, nullable=False)
    notify_role = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
