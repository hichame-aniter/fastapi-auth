from fastapi import FastAPI
from app.routes import admin

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["admin"])