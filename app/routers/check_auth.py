from fastapi import APIRouter, Depends
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/api/auth/check")
def check_auth(current_user: User = Depends(get_current_user)):
    return {
        "message": "認証成功（ログイン済み）",
        "user_id": current_user.user_id,
        "email": current_user.email,
        "name": current_user.name
    }
