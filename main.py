from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi  # ← 追加
from app.auth.auth_router import router as auth_router
from app.routers.signup import router as signup_router
from app.routers.company import router as company_router
from app.routers.job_type import router as job_type_router
from app.routers.job_type_detail import router as job_type_detail_router

app = FastAPI()

# ✅ APIルーター登録
app.include_router(auth_router)
app.include_router(signup_router)
app.include_router(company_router)
app.include_router(job_type_router)
app.include_router(job_type_detail_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

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
