from sqlalchemy.orm import Session
from models.escalation_rule import EscalationRule

def get_active_escalation_rules(db: Session):
    return(
        db.query(EscalationRule).
                 filter(EscalationRule.is_active == True)
                 .order_by(EscalationRule.level)
                 .all()
            )
                 
    