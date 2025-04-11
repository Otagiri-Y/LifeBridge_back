from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.auth_handler import decode_token, oauth2_scheme
from app.models.user import User
from app.db.session import get_db

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user_id_str = decode_token(token)  # JWTのsubに入っているのは user_id（文字列）
    if user_id_str is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user_id in token")

    user = db.query(User).filter(User.user_id == user_id).first()  # user_idベースに変更
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
