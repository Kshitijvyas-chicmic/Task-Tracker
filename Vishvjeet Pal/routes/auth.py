from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.utils.security import get_current_user
from schemas.auth import LoginRequest, Token
from services.activity_log_service import log_activity
from services.auth_service import authenticate_user
from core.utils.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = authenticate_user(db, form_data.username, form_data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    actor_id= get_current_user(token).get("sub")
    log_activity(
        db=db,
        actor_id=actor_id,
        action="login",
        entity="user",
        entity_id=None
    )
    return {"access_token": token}