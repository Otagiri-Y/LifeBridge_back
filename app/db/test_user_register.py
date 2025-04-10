# app/db/test_user_register.py

from app.db.session import get_db
from app.models.user import User
from app.auth.hash import hash_password

def create_test_user():
    db = next(get_db())

    if db.query(User).filter(User.email == "test@example.com").first():
        print("User already exists")
        return

    user = User(
        name="テスト太郎",
        email="test@example.com",
        password=hash_password("password123"),
        address="東京都",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print("✅ ユーザー登録完了:", user.email)

if __name__ == "__main__":
    create_test_user()
