from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.hash import hash_password
from app.db.session import get_db

router = APIRouter()

@router.post("/api/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # 既存メール確認
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています。")

    # パスワードをハッシュ化
    hashed_pw = hash_password(user_data.password)

    # ユーザー作成
    new_user = User(
        name=user_data.name,
        address=user_data.address,
        birth_date=user_data.birth_date,
        email=user_data.email,
        password=hashed_pw,
        last_company="",  # 任意フィールドは空白で登録可
        job_type="",
        job_type_detail=""
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "ユーザー登録が完了しました", "user_id": new_user.user_id}
