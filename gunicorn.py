import multiprocessing
import os

name = "Gunicorn config for FastAPI"

# 環境変数 PORT を取得
port = os.getenv('PORT', '8000')

# 確認用に出力
print(f"Using PORT: {port}")

# バインド設定
bind = f"0.0.0.0:{port}"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1