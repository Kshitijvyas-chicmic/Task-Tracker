# seed/assign_manager.py
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy.orm import Session
from core.utils.deps import get_db
from models import User, Role

def assign_manager(user_email: str, db: Session):
    user = db.query(User).filter(User.email==user_email).first()
    if not user:
        print("User not found")
        return
    manager_role = db.query(Role).filter(Role.name=="manager").first()
    if not manager_role:
        print("Manager role not found")
        return
    user.role = manager_role
    db.commit()
    print(f"{user.name} is now a manager!")

if __name__ == "__main__":
    db = next(get_db())
    assign_manager("manager@gmail.com", db)
