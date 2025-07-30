from app.models.User import User
from fastapi import FastAPI
from app.routes import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])