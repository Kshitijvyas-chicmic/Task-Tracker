from sqlalchemy.orm import Session, joinedload
from models.user import User
from models.role import Role
from core.utils.security import verify_password, create_access_token

def authenticate_user(db: Session, email: str, password: str):
    user = (
    db.query(User)
    .options(
        joinedload(User.role).joinedload(Role.permissions)
    )
    .filter(User.email == email)
    .first()
)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None

    permissions = [perm.name for perm in user.role.permissions] if user.role else []

    token_data = {
        "sub": str(user.e_id),
        "r_id": user.r_id,
        "permissions": permissions
    }
    token = create_access_token(token_data)
    return token
