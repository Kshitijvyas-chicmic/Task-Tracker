import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.utils.deps import SessionLocal
from models.user import User
from core.utils.security import hash_password

db: Session = SessionLocal()
db.execute(text("DELETE FROM users"))
admin = User(
    name="Admin",
    email="admin@gmail.com",
    password=hash_password("admin"),
    r_id=1,
    team="Administration",
    mobile="0000000000"
)

db.add(admin)
db.commit()

print("✅ Admin user created")

db.close()
