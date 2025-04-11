from fastapi import FastAPI
from app.auth.auth_router import router as auth_router
from app.routers.signup import router as signup_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(signup_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

