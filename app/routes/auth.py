from fastapi import APIRouter
from app.models.User import User

router = APIRouter()

@router.post("/signup")
async def signup(user: User, password: str) -> User | str:
    return User.create_user(user, password)

@router.post("/signin")
async def login(email: str, password: str) -> User:
    return User.login_user(email, password)