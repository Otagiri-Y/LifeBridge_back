from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.auth.hash import verify_password
from app.auth.auth_handler import create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter()

class LoginInput(BaseModel):
    email: str
    password: str

@router.post("/api/login")
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/api/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "name": current_user.name
    }
