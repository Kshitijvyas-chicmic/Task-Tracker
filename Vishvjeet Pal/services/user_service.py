from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.utils.security import hash_password
def create_user(db: Session, user_data: UserCreate):
    data = user_data.model_dump()
    print("Password before hash:", data["password"])

    data["password"] = hash_password(data["password"])  # 🔐 hash here

    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, e_id: int):
    return db.query(User).filter(User.e_id == e_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db, user_id: int, data, current_user: dict):
    user = db.query(User).filter(User.e_id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    # Prevent self-role change
    if user_id == int(current_user["sub"]) and "r_id" in data.dict(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot change your own role"
        )

    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db, user_id: int):
    user = db.query(User).filter(User.e_id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}