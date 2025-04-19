from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi  # ← 追加
from app.auth.auth_router import router as auth_router
from app.routers.signup import router as signup_router
from app.routers.company import router as company_router
from app.routers.job_type import router as job_type_router
from app.routers.job_type_detail import router as job_type_detail_router
from app.routers.matching import router as matching_router
# from app.routers.search import router as search_router
from app.routers.check_auth import router as check_auth_router
from fastapi.middleware.cors import CORSMiddleware
# from app.routers.upload import router as upload_router
import os

app = FastAPI()

# CORSの設定（Next.js が localhost:3000 で動作している前提）
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "*"],  # すべてのオリジンを一時的に許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ APIルーター登録
app.include_router(auth_router)
app.include_router(signup_router)
app.include_router(company_router)
app.include_router(job_type_router)
app.include_router(job_type_detail_router)
app.include_router(matching_router)
# app.include_router(search_router)
app.include_router(check_auth_router)
# app.include_router(upload_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# ✅ /test エンドポイント
@app.get("/test")
def test_connection():
    return {"status": "ok", "message": "FastAPI is connected!"}

# ✅ Swagger UI を Bearer 認証に対応させる
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="API description",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # ← 最後に追加
