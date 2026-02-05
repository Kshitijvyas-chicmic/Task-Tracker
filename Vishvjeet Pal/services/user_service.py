from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.utils.security import hash_password
from services.activity_log_service import log_activity

def create_user(db, user_data: UserCreate, actor_id: int):
    user = User(
        name=user_data.name,
        email=user_data.email,
        mobile=user_data.mobile,
        team=user_data.team,
        password=hash_password(user_data.password),
        r_id=user_data.r_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    log_activity(
        db=db,
        actor_id=actor_id,
        action="create_user",
        entity="user",
        entity_id=user.e_id
    )

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