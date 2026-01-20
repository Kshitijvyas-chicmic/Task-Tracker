from fastapi import Depends, HTTPException, status
from core.utils.security import get_current_user

def require_admin(user=Depends(get_current_user)):
    if user.get("role") != 101:   
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

def require_permission(permission_name: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission_name not in [p for p in user.get("permissions", [])]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return user
    return permission_checker
