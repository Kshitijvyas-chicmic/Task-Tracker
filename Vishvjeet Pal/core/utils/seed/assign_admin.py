import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy.orm import Session
from core.utils.deps import get_db
from models import User, Role

def assign_admin(user_email: str, db: Session):
    user = db.query(User).filter(User.email==user_email).first()
    if not user:
        print("User not found")
        return
    admin_role = db.query(Role).filter(Role.name=="Admin").first()
    if not admin_role:
        print("Admin role not found")
        return
    user.role = admin_role
    db.commit()
    print(f"{user.name} is now an admin!")

if __name__ == "__main__":
    db = next(get_db())
    assign_admin("admin@gmail.com", db)
