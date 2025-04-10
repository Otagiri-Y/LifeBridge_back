from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.auth_handler import decode_token, oauth2_scheme
from app.models.user import User
from app.db.session import get_db

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    identifier = decode_token(token)  # emailなど
    if identifier is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == identifier).first()  # ←emailベース
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
