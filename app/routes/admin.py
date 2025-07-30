from fastapi import APIRouter
from app.models.User import User

router = APIRouter()

User.create_user(User(name="Hichame Aniter", email="h.a@gmail.com"), password="passpass")
User.create_user(User(name="Marwa Aniter", email="m.a@gmail.com"), password="passpass")

@router.get("/users")
async def get_users() -> list[User]:
    return User.get_users()

@router.get("/users/{user_id}")
async def get_user(user_id: int, email: str = None):
    return User.get_user(user_id, email)

@router.put("/users/{user_id}/verify-kyc")
async def verify_kyc(user_id: int) -> User:
    return User.verify_kyc(user_id)

@router.put("/users/{user_id}/unverify-kyc")
async def unverify_kyc(user_id: int) -> User:
    return User.unverify_kyc(user_id)


@router.put("/users/{user_id}/ban")
async def ban_user(user_id: int) -> User:
    return User.ban_user(user_id)

@router.put("/users/{user_id}/unban")
async def unban_user(user_id: int) -> User:
    return User.unban_user(user_id)
