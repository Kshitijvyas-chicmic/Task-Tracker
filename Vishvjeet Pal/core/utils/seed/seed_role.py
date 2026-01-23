import sys
from pathlib import Path


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from sqlalchemy.orm import Session
from core.utils.deps import SessionLocal
from models.role import Role
from core.utils.security import hash_password

db: Session = SessionLocal()

admin = Role(
    name="admin",
    r_id=1
)

db.add(admin)
db.commit()

print("✅ Admin role created")

db.close()
