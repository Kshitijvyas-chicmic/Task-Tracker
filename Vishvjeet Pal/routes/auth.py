from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.auth import LoginRequest, Token
from services.auth_service import authenticate_user
from core.utils.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
# def login(data: LoginRequest, db: Session = Depends(get_db)):
#     token = authenticate_user(db, data.email, data.password)
#     if not token:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return {"access_token": token}
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Swagger sends email in `username`
    token = authenticate_user(db, form_data.username, form_data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token}