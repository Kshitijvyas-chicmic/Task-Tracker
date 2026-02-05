import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))

from core.utils.database import SessionLocal 
from models.escalation_rule import EscalationRule

DEFAULT_RULES = [
    {
        "level": 1,
        "after_minutes": 30,
        "action": "email",
        "notify_role": "assignee"
    },
    {
        "level": 2,
        "after_minutes": 60,
        "action": "priority_up",
        "notify_role": "manager"
    },
    {
        "level": 3,
        "after_minutes": 120,
        "action": "reassign",
        "notify_role": "admin"
    }
]

def seed_escalation_rules():
    db = SessionLocal()
    try:
        for rule_data in DEFAULT_RULES:
            exists = (
                db.query(EscalationRule)
                .filter(EscalationRule.level == rule_data["level"])
                .first()
            )

            if exists:
                print(f"Rule level {rule_data['level']} already exists. Skipping...")
                continue

            rule = EscalationRule(**rule_data)
            db.add(rule)
            print(f"Inserted escalation rule level {rule.level}")

        db.commit()
        print("Escalation rules seeding completed 👍")
    except Exception as e:
        db.rollback()
        print("Error seeding escalation rules: ",e)

    finally:
        db.close()

if __name__=="__main__":
    seed_escalation_rules()