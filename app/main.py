from fastapi import FastAPI
from app.routes import admin, auth

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
