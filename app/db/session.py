import os
import tempfile
import platform
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # ローカル開発用（Azure上では不要）

# 環境変数取得
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_SSL_CA_STR = os.getenv("MYSQL_SSL_CA_STR")

# ユーザー名とPython情報を確認
current_user = os.environ.get('USERNAME', '')
python_version = platform.python_version()

# 特定のユーザーとPythonバージョンのみ特別な処理
if current_user == 'takuya.yamaguchi' and python_version.startswith('3.13'):
    # SSL検証をスキップするモードで接続
    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        f"?ssl=true&ssl_verify_cert=false"
    )
else:
    # 通常の接続方法（他の開発者用）
    # SSL証明書の文字列から改行を復元
    ssl_cert_content = MYSQL_SSL_CA_STR.replace("\\n", "\n")

    # 一時ファイルとして証明書を書き出し
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as temp_cert_file:
        temp_cert_file.write(ssl_cert_content.encode())
        ssl_cert_path = temp_cert_file.name

    # SQLAlchemy 接続文字列を構築
    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        f"?ssl_ca={ssl_cert_path}"
    )

# SQLAlchemy セッション作成
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()